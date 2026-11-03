"""Profile permissions, durable drafts and live host execution boundaries."""
import tempfile
import unittest
from pathlib import Path
from agent.subagent_profiles import SubagentProfiles, READS


class SubagentProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=SubagentProfiles(Path(self.temp.name))

    def fields(self):
        return {'title':'Аудитор','summary':'Исследовать архитектуру','instructions':'Прочитай файл и верни подтверждённые факты.','tools':['read_range']}

    def test_generated_draft_survives_restart_and_requires_user_enablement(self):
        item=self.store.configure(self.fields(),generated=True)
        self.assertFalse(item['enabled']);self.assertEqual(item['source'],'model')
        with self.assertRaises(ValueError):self.store.resolve(item['id'])
        fresh=SubagentProfiles(Path(self.temp.name))
        self.assertIn(item,fresh.catalog()['profiles'])
        edited=fresh.configure({'kind':'subagent_save',**item,'enabled':True})
        self.assertEqual(edited['version'],2);self.assertEqual(fresh.resolve(item['id'])['tools'],['read_range'])
        fresh.configure({'kind':'subagent_delete','id':item['id']})
        with self.assertRaises(ValueError):fresh.resolve(item['id'])

    def test_model_cannot_overwrite_enable_or_add_capabilities(self):
        for values in ({'enabled':True},{'id':'research'},{'model':'other'},{'tools':['write_file']},{'tools':['mcp_run']},{'tools':['read_range','read_range']}):
            with self.subTest(values=values),self.assertRaises(ValueError):self.store.configure({**self.fields(),**values},generated=True)
        self.assertEqual(len(self.store.catalog()['profiles']),1)
        self.store.configure({'kind':'subagents_toggle','enabled':False})
        with self.assertRaises(ValueError):self.store.configure(self.fields(),generated=True)
        with self.assertRaises(ValueError):self.store.resolve('research')

    def test_corruption_fails_closed_and_catalog_copies_cannot_grant_rights(self):
        data=self.store.catalog();data['profiles'][0]['tools'].append('write_file')
        self.assertEqual(set(self.store.resolve('research')['tools']),READS)
        self.store.path.write_text('{"version":200}',encoding='utf8')
        with self.assertRaises(ValueError):self.store.catalog()
