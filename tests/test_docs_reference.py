"""The reference inventories vendored files without treating them as application API."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import generate_code_reference as reference


class ReferenceInventoryTests(unittest.TestCase):
    """Check both the inventory and the AST extractor inputs."""
    def test_vendor_is_in_inventory_but_not_in_ast_or_toc(self):
        """Only the reviewed vendor path is excluded; current application sources remain documented."""
        vendor = 'codex-skills.mjs'
        source = 'apps/desktop/src/ideEntry.ts'
        with patch.object(reference, 'repository_files', return_value=[vendor, source]), \
             patch.object(reference, 'FILE_NOTES', {vendor: 'Vendor CLI', source: 'IDE entry'}), \
             patch.object(reference, 'SYMBOL_NOTES', {}), \
             patch.object(reference, 'TS_NOTES', {}), \
             patch.object(reference.subprocess, 'run') as extract:
            extract.return_value.stdout = json.dumps([{'file': source, 'symbols': []}])
            documents = reference.render()
        self.assertIn(vendor, documents['docs/reference/file-map.md'])
        self.assertNotIn(vendor, documents['docs/reference/typescript.md'])
        self.assertIn(source, documents['docs/reference/typescript.md'])
        self.assertEqual(json.loads(extract.call_args.kwargs['input']), [source])
