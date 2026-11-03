"""Saved-source selection, budgeting and explicit remote approval without remote network traffic."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import httpx
from agent import task_store
from agent.context_builder import ContextBuilder,PACK_MARKER,pack_message,pack_summary,validate_context,local_context_endpoint
from agent.model_client import ModelClient,SourceContextApprovalError
from agent.project_index import get_index,close_indexes
from agent.request_budget import RequestBudget,prepare_model_request


class ContextBuilderTests(unittest.TestCase):
    """All sources/profile state belong to an isolated temporary project."""
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.base=Path(temp.name);self.root=self.base/'project';self.root.mkdir()
        self.scope=patch.object(task_store,'TASK_DIR',self.base/'profile/tasks');self.scope.start();self.addCleanup(self.scope.stop);self.addCleanup(close_indexes)
        (self.root/'app').mkdir();(self.root/'tests').mkdir()
        (self.root/'app/main.py').write_text('def calculate_total(amount):\n    return amount * 1.2\n',encoding='utf-8')
        (self.root/'tests/test_main.py').write_text('def test_total():\n    assert True\n',encoding='utf-8')
        self.builder=ContextBuilder(self.root)

    def params(self):
        """A mandatory current request and a selected, optional saved-source pack."""
        return self.builder.project({'model':'fixture','stream':True,'max_tokens':256,'messages':[
            {'role':'system','content':'Rules'},{'role':'user','content':'Explain app/main.py'}]},'Explain app/main.py')

    def test_ephemeral_pack_and_anchors_keep_canonical_history_untouched(self):
        original={'messages':[{'role':'system','content':'Rules'},{'role':'user','content':'app/main.py'}]};before=deepcopy(original)
        selected=self.builder.project(original,'app/main.py:2')
        self.assertEqual(original,before);self.assertEqual(selected['messages'][-1],original['messages'][-1])
        source=selected['messages'][1][PACK_MARKER]['sources'][0]
        self.assertEqual(source['source_kind'],'saved-file');self.assertEqual(len(source['sha256']),64)
        self.assertEqual(source['start_line'],1);self.assertEqual(source['end_line'],2)
        wire=prepare_model_request({**selected,'model':'fixture'})
        self.assertTrue(all(PACK_MARKER not in m for m in wire['messages']));self.assertNotIn(str(self.root),json.dumps(wire))
        self.assertIn('calculate_total',wire['messages'][1]['content']);self.assertNotIn('calculate_total',wire['messages'][0]['content'])

    def test_automatic_rollout_keeps_measured_json_regression_disabled(self):
        from agent.engine import AgentEngine
        for protocol,remote,approve,enabled in (('json',False,False,False),('native',False,False,True),('native',True,False,False),('native',True,True,True)):
            with self.subTest(protocol=protocol,remote=remote,approve=approve):
                engine=AgentEngine('https://example.invalid/v1' if remote else 'http://127.0.0.1:1234/v1','', 'fixture',str(self.root),'app/main.py',
                    tool_protocol=protocol,source_approval=(lambda _text:False) if approve else None)
                self.assertEqual(isinstance(engine.context_builder,ContextBuilder),enabled)
        disabled=AgentEngine('http://127.0.0.1:1234/v1','','fixture',str(self.root),'app/main.py',tool_definitions=[])
        self.assertIsNone(disabled.context_builder)

    def test_index_selects_symbol_and_related_test_without_duplicate_ranges(self):
        index=get_index(self.root,create=True);deadline=time.monotonic()+15
        while index.state!='ready' and time.monotonic()<deadline:time.sleep(.025)
        pack=self.builder.build('Find calculate_total in app/main.py',[])
        paths=[s['path'] for s in pack['sources']]
        self.assertEqual(paths.count('app/main.py'),1);self.assertIn('tests/test_main.py',paths)
        self.assertEqual(pack['sources'][0]['reason'],'Файл явно указан в запросе')

    def test_policy_and_content_rechecked_after_selection(self):
        params=self.params();messages=params['messages']
        (self.root/'app/main.py').write_text('changed',encoding='utf-8')
        self.assertFalse(pack_summary(validate_context(messages,self.root))['sources'])
        params=self.params();(self.root/'.neutralignore').write_text('app/**\n',encoding='utf-8')
        self.assertFalse(pack_summary(validate_context(params['messages'],self.root))['sources'])
        self.assertFalse(self.builder.build('app/main.py',[])['sources'])

    def test_existing_visible_read_is_not_duplicated_but_changed_content_is_selected(self):
        content=(self.root/'app/main.py').read_text(encoding='utf-8')
        messages=[{'role':'tool','content':json.dumps({'ok':True,'path':'app/main.py','content':content})}]
        self.assertFalse(self.builder.build('app/main.py',messages)['sources'])
        (self.root/'app/main.py').write_text('def changed():\n    return 2\n',encoding='utf-8')
        self.assertTrue(self.builder.build('app/main.py',messages)['sources'])

    def test_unchanged_fragment_does_not_reuse_an_obsolete_whole_file_hash(self):
        from agent.workspace_read import read_range
        source=self.root/'app/main.py';source.write_text('first line\n'+'unchanged\n'*80,encoding='utf-8')
        receipt=read_range(self.root,'app/main.py',1,13)
        source.write_text(source.read_text(encoding='utf-8')+'changed outside range\n',encoding='utf-8')
        pack=self.builder.build('app/main.py',[{'role':'tool','content':json.dumps(receipt)}])
        self.assertTrue(pack['sources']);self.assertNotEqual(pack['sources'][0]['sha256'],receipt['sha256'])

    def test_denied_missing_foreign_and_cancelled_sources(self):
        (self.root/'.env').write_text('SYNTHETIC_SECRET=never-send')
        (self.root/'.gitignore').write_text('private.py\n');(self.root/'private.py').write_text('PRIVATE')
        pack=self.builder.build('private.py missing.py ../../outside.py .env',[])
        self.assertFalse(pack['sources'])
        message=self.params()['messages'][1];message[PACK_MARKER]['root']=str(self.base)
        self.assertFalse(pack_summary(validate_context([message],self.root))['sources'])
        stop=threading.Event();stop.set()
        with self.assertRaises(InterruptedError):ContextBuilder(self.root,stop).build('app/main.py',[])

    def test_grant_revocation_hides_sources_and_invalidates_pack(self):
        from agent.workspace_access import WorkspaceAccessPolicy
        from agent.context_builder import visible_summary
        (self.root/'.neutralignore').write_text('app/main.py\n',encoding='utf-8')
        WorkspaceAccessPolicy(self.root).configure(['app/main.py'],True)
        messages=self.params()['messages'];summary=pack_summary(messages)
        self.assertEqual(len(summary['sources']),1)
        WorkspaceAccessPolicy(self.root).configure([],True)
        self.assertFalse(pack_summary(validate_context(messages,self.root))['sources'])
        self.assertFalse(visible_summary(summary,self.root)['sources'])

    def test_budget_drops_whole_fragments_before_current_prompt(self):
        params=self.params();source=params['messages'][1][PACK_MARKER]['sources'][0]
        sources=[{**source,'path':f'file-{i}.py','content':'🧩'*5000} for i in range(12)]
        params['messages'][1]=pack_message({**params['messages'][1][PACK_MARKER],'sources':sources})
        before=deepcopy(params);budget=RequestBudget(4096,256)
        fitted,stats=budget.fit(params,protected_text=params['messages'][-1]['content'])
        self.assertEqual(stats['context_sources_dropped'],12)
        self.assertFalse(pack_summary(fitted['messages'])['sources'])
        self.assertEqual(fitted['messages'][-1],params['messages'][-1]);self.assertEqual(params,before)
        for message in fitted['messages']:
            if PACK_MARKER in message:json.loads(message['content'])
        budget.check(prepare_model_request(fitted),())

    def test_optional_sources_do_not_displace_available_tool_schemas(self):
        from tests.test_request_budget import definition
        params=self.params();params['tools']=[definition('tool_'+str(i)) for i in range(8)]
        source=params['messages'][1][PACK_MARKER]['sources'][0]
        source['content']='🧩'*5000;params['messages'][1]=pack_message(params['messages'][1][PACK_MARKER])
        fitted,stats=RequestBudget(4096,256,mode='auto').fit(params,protected_text=params['messages'][-1]['content'])
        self.assertEqual(stats['context_sources_dropped'],1);self.assertEqual(stats['tools_deferred'],0)
        self.assertEqual(fitted['tools'],params['tools'])

    def client(self,remote=True):
        """Construct SDK transport but never contact the configured external hostname."""
        client=ModelClient('https://example.invalid/v1' if remote else 'http://127.0.0.1:1234/v1','',threading.Event())
        self.addCleanup(client.close);client.context_root=str(self.root)
        return client

    def send(self,client,callback=None,fail_first=False):
        """Exercise the actual per-attempt guard against an in-memory endpoint."""
        params=self.params();params['stream']=False;client.source_approval=callback;sent=[]
        async def create(**request):
            sent.append(request)
            if fail_first and len(sent)==1:
                from openai import InternalServerError
                raise InternalServerError('retry',response=httpx.Response(500,request=httpx.Request('POST','https://example.invalid/v1/chat/completions')),body={})
            return SimpleNamespace(ok=True)
        result=client.result(client.submit(client.request(SimpleNamespace(create=create),prepare_model_request(params),params)))
        return result,sent

    def test_remote_requires_concrete_approval_and_has_no_redirects_or_proxy(self):
        client=self.client();proposals=[]
        def approve(text):
            proposal=json.loads(text);proposals.append(proposal)
            self.assertEqual(proposal['recipient'],'https://example.invalid/v1/chat/completions')
            self.assertEqual(proposal['model'],'fixture');self.assertIn('calculate_total',proposal['sources'][0]['content'])
            return True
        _,sent=self.send(client,approve,fail_first=True)
        self.assertEqual(len(sent),2);self.assertEqual(len(proposals),2)
        self.assertTrue(all(PACK_MARKER not in m for request in sent for m in request['messages']));self.assertFalse(client.client._client.follow_redirects)
        self.assertFalse(client.client._client._trust_env)

    def test_rejection_and_edit_during_preview_never_reach_endpoint(self):
        for change in (False,True):
            with self.subTest(change=change):
                client=self.client()
                def approve(_text):
                    if change:(self.root/'app/main.py').write_text('changed',encoding='utf-8')
                    return change
                with self.assertRaises(SourceContextApprovalError):self.send(client,approve)

    def test_destination_change_during_approval_requires_new_preview(self):
        client=self.client()
        def approve(_text):
            client.base_url='https://other.invalid/v1'
            return True
        with self.assertRaises(SourceContextApprovalError):self.send(client,approve)

    def test_no_callback_strips_remote_pack_but_loopback_validates_it(self):
        _,remote=self.send(self.client())
        self.assertNotIn('calculate_total',json.dumps(remote))
        _,local=self.send(self.client(False))
        self.assertIn('calculate_total',json.dumps(local))
        self.assertFalse(local_context_endpoint('http://192.168.1.2:1234'))
        self.assertTrue(local_context_endpoint('http://[::1]:1234/v1'))

    def test_local_retry_omits_changed_sources(self):
        client=self.client(False);params=self.params();params['stream']=False;sent=[]
        async def create(**request):
            sent.append(request)
            if len(sent)==1:
                (self.root/'app/main.py').write_text('changed',encoding='utf-8')
                from openai import InternalServerError
                raise InternalServerError('retry',response=httpx.Response(500,request=httpx.Request('POST','http://127.0.0.1/v1/chat/completions')),body={})
            return None
        client.result(client.submit(client.request(SimpleNamespace(create=create),prepare_model_request(params),params)))
        self.assertIn('calculate_total',json.dumps(sent[0]));self.assertNotIn('calculate_total',json.dumps(sent[1]))

