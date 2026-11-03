import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent import project_memory
from core.python.memory_service import read_memory, write_memory


class MemoryServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)/'project';self.root.mkdir();self.root=self.root.resolve()
        self.patch=patch.object(project_memory,'MEMORY_DIR',Path(self.temp.name)/'store');self.patch.start()

    def tearDown(self):
        self.patch.stop();self.temp.cleanup()

    def test_round_trip_and_external_update_preserve_stale_draft(self):
        original=read_memory(self.root)
        fields={**original['memory'],'project_summary':'Проект'}
        saved=write_memory(self.root,{'memory':fields,'revision':original['revision']})
        self.assertEqual(saved['memory']['project_summary'],'Проект')
        self.assertNotEqual(saved['revision'],original['revision'])
        project_memory.save_project_memory(str(self.root),{'current_focus':'Модель обновила память'})
        with self.assertRaisesRegex(ValueError,'MEMORY_CHANGED'):
            write_memory(self.root,{'memory':fields,'revision':saved['revision']})
        self.assertEqual(read_memory(self.root)['memory']['current_focus'],'Модель обновила память')

    def test_invalid_fields_do_not_modify_store(self):
        original=read_memory(self.root)
        for changed in ({'project_summary':4},{'next_steps':'x'*801},{'decisions':['x']*31},{'constraints':'bad'},{'extra':'bad'}):
            with self.assertRaises(ValueError):write_memory(self.root,{'memory':{**original['memory'],**changed},'revision':original['revision']})
        self.assertFalse(project_memory.memory_path(str(self.root)).exists())

    def test_corrupt_memory_is_preserved_and_other_project_is_isolated(self):
        path=project_memory.memory_path(str(self.root));path.parent.mkdir(parents=True);path.write_bytes(b'{broken')
        with self.assertRaises(ValueError):read_memory(self.root)
        self.assertEqual(path.read_bytes(),b'{broken')
        other=self.root.parent/'other';other.mkdir()
        self.assertEqual(read_memory(other)['memory']['project_summary'],'')

    def test_full_unicode_budget_is_readable(self):
        fields={key:'😀'*limit for key,limit in project_memory.FIELDS.items()}
        fields.update({key:[('😀'*(limit-3))+str(i) for i in range(count)] for key,(count,limit) in project_memory.LIST_FIELDS.items()})
        original=read_memory(self.root)
        result=write_memory(self.root,{'memory':fields,'revision':original['revision']})
        self.assertEqual(result['memory']['project_summary'],fields['project_summary'])
