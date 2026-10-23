import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from core.python.project_search import ProjectSearchService, search_project


class ProjectSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'src').mkdir()
        (self.root / 'src' / 'Пример.py').write_text('first\nNeedle строка\nneedle again\n', encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def test_literal_text_line_case_and_path_filter(self):
        result = search_project(self.root, {'query':'NEEDLE','pattern':'*.py'})
        self.assertEqual([m['line'] for m in result['matches']], [2,3])
        self.assertEqual(result['matches'][0]['path'], 'src/Пример.py')
        self.assertEqual(len(search_project(self.root, {'query':'Needle','case_sensitive':True})['matches']), 1)
        self.assertFalse(search_project(self.root, {'query':'Needle','pattern':'*.txt'})['matches'])
        self.assertFalse(search_project(self.root, {'query':'.*'})['matches'])

    def test_files_ignored_binary_encoding_size_and_result_limits(self):
        (self.root / 'node_modules').mkdir()
        (self.root / 'node_modules' / 'hidden.py').write_text('Needle')
        (self.root / 'binary').write_bytes(b'Needle\x00')
        (self.root / 'invalid').write_bytes(b'Needle\xff')
        (self.root / 'large').write_bytes(b'x' * 1_000_001)
        result=search_project(self.root, {'query':'needle'})
        self.assertEqual(len(result['matches']), 2)
        self.assertEqual(result['skipped_files'], 3)
        paths=search_project(self.root, {'mode':'files','query':'ПРИМЕР'})
        self.assertEqual(len(paths['matches']),1)
        limited=search_project(self.root, {'query':'needle','limit':1})
        self.assertEqual(len(limited['matches']),1)
        self.assertEqual(limited['reason'],'results')

    def test_cancel_time_and_budget_are_reported(self):
        cancelled=threading.Event();cancelled.set()
        self.assertEqual(search_project(self.root, {'query':'Needle'},cancelled)['code'],'SEARCH_CANCELLED')
        self.assertEqual(search_project(self.root, {'query':'Needle'},timeout=0)['reason'],'time')
        self.assertEqual(search_project(self.root, {'query':'Needle'},max_bytes=1)['reason'],'bytes')
        self.assertEqual(search_project(self.root, {'query':'Needle'},max_files=0)['reason'],'files')
        for params in ({'query':''},{'query':'a','limit':True},{'query':'x','case_sensitive':'yes'},{'mode':'bad'}):
            with self.assertRaises(ValueError): search_project(self.root,params)

    def test_symlink_cannot_expand_search_scope(self):
        with tempfile.TemporaryDirectory() as other:
            outside=Path(other)/'outside.txt';outside.write_text('SECRET')
            try: (self.root/'link.txt').symlink_to(outside)
            except OSError: self.skipTest('Symlink privilege unavailable')
            self.assertFalse(search_project(self.root,{'query':'SECRET'})['matches'])

    def test_worker_cancellation_single_flight_and_invalid_root_recovery(self):
        service=ProjectSearchService();entered=threading.Event();release=threading.Event();responses=[]
        def slow(root,params,cancelled):
            entered.set();release.wait(2)
            return {'ok':not cancelled.is_set()}
        with self.assertRaises(FileNotFoundError): service.start(self.root/'missing',{},responses.append)
        self.assertFalse(service.running)
        with patch('core.python.project_search.search_project',side_effect=slow):
            service.start(self.root,{'query':'x'},responses.append)
            self.assertTrue(entered.wait(1))
            with self.assertRaises(ValueError): service.start(self.root,{},responses.append)
            service.cancel();release.set();service.shutdown()
        self.assertEqual(responses,[{'ok':False}])
        self.assertFalse(service.running)
