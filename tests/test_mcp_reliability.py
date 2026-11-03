"""MCP endpoint identity, legacy denial migration and discovery lifetime regressions."""
import hashlib
import json
import queue
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from core.python.extension_service import ExtensionService, mcp_alias


TOOL={'name':'echo','description':'Fixture','parameters':{'type':'object'}}


class MCPReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.service=ExtensionService(self.temp.name)
        self.addCleanup(self.service.shutdown)

    def add_server(self, identity='echo', **options):
        self.service.configure({'kind':'server_save','server':{'id':identity,'command':sys.executable,'enabled':True,**options}})
        return self.service.state['servers'][-1]

    def test_full_endpoint_alias_separates_long_prefixes_and_connections(self):
        first=self.add_server('same_server_prefix_123456_one')
        second=self.add_server('same_server_prefix_123456_two')
        self.assertNotEqual(mcp_alias(first,'echo'),mcp_alias(second,'echo'))
        self.assertNotEqual(mcp_alias(first,'echo'),mcp_alias({**first,'args':['different']},'echo'))
        with patch.object(self.service.mcp,'operation',return_value={'ok':True,'tools':[TOOL]}):
            self.service.discover_server(first['id']);self.service.discover_server(second['id'])
        snapshot=self.service.snapshot([])
        routes=snapshot['external']
        self.assertEqual(len(routes),2)
        self.assertEqual({r['server']['id'] for r in routes.values()},{first['id'],second['id']})

    def test_migrate_legacy_collision_preserves_disabled_tools_and_plugin_links(self):
        servers=[self.add_server('same_server_prefix_123456_'+suffix) for suffix in ('one','two')]
        old='mcp_'+servers[0]['id'][:25]+'_'+hashlib.sha256(b'echo').hexdigest()[:12]
        for server in servers:server['tools']=[{**TOOL,'id':old}]
        self.service.state['tools'][old]=False
        self.service.state['plugins']=[{'id':'old','tools':[old],'skills':[],'servers':[],'enabled':False}]
        self.service.save()
        migrated=ExtensionService(self.temp.name)
        aliases={mcp_alias(server,'echo') for server in servers}
        self.assertEqual(len(aliases),2)
        self.assertEqual(set(migrated.state['plugins'][0]['tools']),aliases)
        self.assertTrue(all(migrated.state['tools'][alias] is False for alias in aliases))
        self.assertEqual(migrated.snapshot([])['external'],{})
        enabled=next(iter(aliases))
        migrated.configure({'kind':'tools','id':enabled,'enabled':True})
        self.assertEqual(set(migrated.snapshot([])['external']),{enabled})
        reloaded=ExtensionService(self.temp.name)
        self.assertEqual(set(reloaded.snapshot([])['external']),{enabled})

    def test_duplicate_names_are_rejected_before_overwriting_previous_catalog(self):
        server=self.add_server()
        with patch.object(self.service.mcp,'operation',return_value={'ok':True,'tools':[TOOL]}):
            self.service.discover_server(server['id'])
        before=json.dumps(server['tools'])
        with patch.object(self.service.mcp,'operation',return_value={'ok':True,'tools':[TOOL,TOOL]}):
            with self.assertRaisesRegex(ValueError,'повторяющееся'):self.service.discover_server(server['id'])
        self.assertEqual(json.dumps(server['tools']),before)

    def test_single_discovery_is_cancellable_and_does_not_publish_late_tools(self):
        self.add_server()
        started=threading.Event();answers=queue.Queue();calls=[]
        def operation(*_,interrupted=None,**kwargs):
            calls.append(1);started.set()
            if not interrupted.wait(3):raise AssertionError('Cancellation was not delivered')
            return {'ok':True,'tools':[TOOL]}
        with patch.object(self.service.mcp,'operation',side_effect=operation):
            self.service.start_discovery('echo',answers.put)
            self.assertTrue(started.wait(1))
            with self.assertRaisesRegex(ValueError,'уже выполняется'):self.service.start_discovery('echo',answers.put)
            self.assertEqual(self.service.cancel_discovery('echo')['cancelled'],1)
            result=answers.get(timeout=2)
        self.assertTrue(result['canceled']);self.assertFalse(result['ok'])
        self.assertEqual(len(calls),1);self.assertNotIn('tools',self.service.state['servers'][0])
        self.assertEqual(self.service.discoveries,{})

    def test_shutdown_cancels_workers_and_rejects_new_discovery(self):
        self.add_server();started=threading.Event();answers=queue.Queue()
        def operation(*_,interrupted=None,**kwargs):
            started.set();interrupted.wait(3)
            return {'ok':False,'error':'cancelled'}
        with patch.object(self.service.mcp,'operation',side_effect=operation):
            self.service.start_discovery('echo',answers.put);self.assertTrue(started.wait(1))
            self.service.shutdown()
        self.assertTrue(answers.get(timeout=1)['canceled'])
        self.assertEqual(self.service.discoveries,{})
        with self.assertRaisesRegex(ValueError,'завершаются'):self.service.start_discovery('echo',answers.put)

    def test_real_stdio_discovery_can_finish_after_old_ten_second_deadline(self):
        fixture=str(Path(__file__).parent/'fixtures/mcp_echo.py')
        bootstrap="import time,runpy,sys;time.sleep(11);p=sys.argv[1];sys.argv=[p];runpy.run_path(p,run_name='__main__')"
        self.add_server(args=['-c',bootstrap,fixture],timeout=30)
        answers=queue.Queue();started=time.monotonic()
        self.service.start_discovery('echo',answers.put)
        result=answers.get(timeout=25)
        self.assertTrue(result['ok'],result)
        self.assertGreater(time.monotonic()-started,10)
        self.assertEqual(len(result['tools']),3)


if __name__=='__main__':unittest.main()
