import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.python.editor_service import EditorService
from agent.tools import preview_file_change


class EditorServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.file = self.root / 'text.txt'
        self.file.write_bytes(b'first\r\nsecond\r\n')
        self.service = EditorService()

    def tearDown(self):
        self.temp.cleanup()

    def proposal(self, content='edited\nsecond\n'):
        document = self.service.read(self.root, 'text.txt')
        return self.service.preview(self.root, {'path':'text.txt','content':content,'revision':document['revision']})

    def test_read_preview_and_one_shot_apply_preserve_crlf(self):
        document = self.service.read(self.root, 'text.txt')
        self.assertEqual(document['content'], 'first\nsecond\n')
        self.assertEqual(document['newline'], 'crlf')
        self.assertEqual(document['revision']['sha256'], hashlib.sha256(self.file.read_bytes()).hexdigest())
        proposal = self.proposal()
        self.assertIn('+edited', proposal['diff'])
        self.assertEqual(self.file.read_bytes(), b'first\r\nsecond\r\n')
        result = self.service.resolve(self.root, {'proposal_id':proposal['proposal_id'],'decision':'apply'})
        self.assertTrue(result['applied'])
        self.assertEqual(self.file.read_bytes(), b'edited\r\nsecond\r\n')
        self.assertNotEqual(document['revision'], result['file']['revision'])
        with self.assertRaises(ValueError):
            self.service.resolve(self.root, {'proposal_id':proposal['proposal_id'],'decision':'apply'})

    def test_external_change_before_preview_and_after_approval_is_never_overwritten(self):
        document = self.service.read(self.root, 'text.txt')
        self.file.write_text('external', encoding='utf-8')
        result = self.service.preview(self.root, {'path':'text.txt','content':'draft','revision':document['revision']})
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertIsNone(self.service.pending)
        proposal = self.proposal('new draft')
        self.file.write_text('external again', encoding='utf-8')
        result = self.service.resolve(self.root, {'proposal_id':proposal['proposal_id'],'decision':'apply'})
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertEqual(self.file.read_text(), 'external again')
        self.assertIsNone(self.service.pending)

    def test_reject_cancel_and_replaced_proposals_do_not_write(self):
        for decision in ('reject','cancel'):
            proposal = self.proposal()
            self.assertFalse(self.service.resolve(self.root, {'proposal_id':proposal['proposal_id'],'decision':decision})['applied'])
            self.assertEqual(self.file.read_bytes(), b'first\r\nsecond\r\n')
        old = self.proposal()
        self.proposal('different')
        with self.assertRaises(ValueError):
            self.service.resolve(self.root, {'proposal_id':old['proposal_id'],'decision':'apply'})
        self.assertEqual(self.file.read_bytes(), b'first\r\nsecond\r\n')

    def test_unchanged_text_has_no_pending_write(self):
        result = self.proposal('first\nsecond\n')
        self.assertTrue(result['unchanged'])
        self.assertIsNone(self.service.pending)

    def test_editor_can_save_files_up_to_one_mb_and_recheck_conflicts(self):
        original = b'a' * 999_999 + b'\n'
        self.file.write_bytes(original)
        self.assertFalse(preview_file_change(self.root, 'text.txt', 'agent draft')['ok'])
        proposal = self.proposal('b' + original[1:].decode())
        self.assertTrue(proposal['ok'], proposal)
        result = self.service.resolve(self.root, {'proposal_id':proposal['proposal_id'],'decision':'apply'})
        self.assertTrue(result['applied'], result)
        self.assertEqual(self.file.read_bytes(), b'b' + original[1:])
        proposal = self.proposal('c' + original[1:].decode())
        self.file.write_bytes(original)
        result = self.service.resolve(self.root, {'proposal_id':proposal['proposal_id'],'decision':'apply'})
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertEqual(self.file.read_bytes(), original)

    def test_change_between_revision_check_and_diff_does_not_authorize_stale_draft(self):
        document = self.service.read(self.root, 'text.txt')
        def external_change(*args, **kwargs):
            self.file.write_text('external edit', encoding='utf-8')
            return preview_file_change(*args, **kwargs)
        with patch('core.python.editor_service.preview_file_change', side_effect=external_change):
            result = self.service.preview(self.root, {'path':'text.txt','content':'stale draft','revision':document['revision']})
        self.assertEqual(result.get('code'), 'FILE_CHANGED', result)
        self.assertIsNone(self.service.pending)
        self.assertEqual(self.file.read_text(), 'external edit')

    def test_outside_binary_invalid_utf8_and_large_files_are_rejected(self):
        outside = Path(self.temp.name) / 'outside.txt'
        outside.write_text('outside')
        with self.assertRaises(PermissionError):
            self.service.read(self.root, '../outside.txt')
        for raw in (b'\xff', b'a\x00b', b'x' * 1_000_001):
            self.file.write_bytes(raw)
            with self.assertRaises(ValueError):
                self.service.read(self.root, 'text.txt')
        self.assertEqual(outside.read_text(), 'outside')

    def test_proposal_cannot_be_applied_to_another_project(self):
        proposal = self.proposal()
        other = Path(self.temp.name) / 'other'
        other.mkdir()
        (other / 'text.txt').write_text('other')
        with self.assertRaises(ValueError):
            self.service.resolve(other, {'proposal_id':proposal['proposal_id'],'decision':'apply'})
        self.assertEqual((other / 'text.txt').read_text(), 'other')
