"""Real Core HTTP sessions reuse fresh project memory and keep proposals hypothetical."""
import json
import unittest
from http.server import BaseHTTPRequestHandler
from tests.migration import test_run_control as fixture
from core.python.memory_service import read_memory,memory_action
from agent.project_knowledge import ProjectKnowledge


class MemoryHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"data":[{"id":"fixture"}]}')
    def do_POST(self):
        p=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.requests.append(p)
        if not p.get('stream'):
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(json.dumps({'choices':[{'message':{'content':'{"complete":true}'},'finish_reason':'stop'}]}).encode());return
        prompt=next(m['content'] for m in reversed(p['messages']) if m['role']=='user')
        tools=[m for m in p['messages'] if m.get('role')=='tool'];delta={'content':'Ответ с опорой на источники.'}
        if getattr(self.server,'search_memory',False) and not tools:
            delta={'tool_calls':[{'index':0,'id':'search-memory','type':'function','function':{'name':'search_project_memory','arguments':'{"query":"VALUE"}'}}]}
        if 'Прочитай' in prompt and len(tools)<2:
            name,args=('read_range',{'path':'main.py','start_line':1,'end_line':1}) if not tools else ('remember_project_note',{'text':'VALUE используется для вычислений','paths':['main.py']})
            delta={'tool_calls':[{'index':0,'id':'memory'+str(len(tools)),'type':'function','function':{'name':name,'arguments':json.dumps(args)}}]}
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        self.wfile.write(('data: '+json.dumps({'choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if 'tool_calls' in delta else 'stop'}]})+'\n\ndata: [DONE]\n\n').encode())


class ProjectMemoryHttpTests(unittest.TestCase):
    setUp=fixture.RunControlHttpTests.setUp
    stop_server=fixture.RunControlHttpTests.stop_server
    event=fixture.RunControlHttpTests.event

    def start(self,prompt):
        self.server.RequestHandlerClass=MemoryHandler;self.service.config['tool_protocol']='native';self.service.config['settings']['memory_updates']='on_change'
        self.service.start(self.root,{'mode':'ide','prompt':prompt});self.event('task_end');self.service.thread.join(5)
        self.assertEqual(self.service.chat['task_checkpoint']['run_state'],'completed')

    def test_new_chat_receives_decision_and_hypothesis_but_changed_source_removes_both(self):
        (self.root/'main.py').write_text('VALUE = 1\n')
        initial=read_memory(self.root)
        memory_action(self.root,{'root':str(self.root),'revision':initial['revision'],'action':'save','record':{'kind':'decision','text':'PRIVATE_VALUE_DECISION: использовать VALUE для расчёта','paths':['main.py']}})
        self.start('Прочитай main.py и сохрани вывод о VALUE')
        records=ProjectKnowledge(self.root).listing();self.assertTrue(any(r['origin']=='model' and r['kind']=='hypothesis' for r in records));self.assertTrue(any(r['origin']=='tool' for r in records))
        old_chat=self.service.chat['id'];self.service.select_chat(self.root)
        self.assertNotEqual(self.service.chat['id'],old_chat)
        before=len(self.server.requests);self.start('Объясни решение о VALUE')
        system=json.dumps(self.server.requests[before]['messages'],ensure_ascii=False);self.assertIn('PRIVATE_VALUE_DECISION',system);self.assertIn('hypothesis',system)
        (self.root/'main.py').write_text('VALUE = 2\n');self.service.select_chat(self.root)
        before=len(self.server.requests);self.start('Объясни решение о VALUE')
        self.assertNotIn('PRIVATE_VALUE_DECISION',json.dumps(self.server.requests[before]['messages'],ensure_ascii=False))
        self.assertEqual(self.service.chat['task_checkpoint']['run_state'],'completed')


    def test_disabling_memory_group_removes_tools_and_automatic_projection(self):
        (self.root/'main.py').write_text('VALUE = 1\n')
        ProjectKnowledge(self.root).put({'text':'PRIVATE_VALUE_DECISION','kind':'decision','paths':['main.py']})
        self.service.extensions.configure({'kind':'groups','id':'memory','enabled':False})
        self.start('Объясни решение о VALUE')
        payload=self.server.requests[0]
        names={t['function']['name'] for t in payload.get('tools',[])}
        self.assertFalse({'search_project_memory','remember_project_note'} & names)
        self.assertNotIn('PRIVATE_VALUE_DECISION',json.dumps(payload))


    def test_external_memory_preview_is_text_and_rejection_keeps_data_out_of_model(self):
        from unittest.mock import patch
        from agent.engine import AgentEngine
        self.service.engine_factory=lambda **kwargs:AgentEngine(context_builder=False,**kwargs)
        (self.root/'main.py').write_text('VALUE = 1\n')
        ProjectKnowledge(self.root).put({'text':'PRIVATE_VALUE_DECISION','kind':'decision','paths':['main.py']})
        self.server.RequestHandlerClass=MemoryHandler;self.server.search_memory=True;self.service.config['tool_protocol']='native'
        with patch('agent.auto_budget.local_endpoint',return_value=False),patch('agent.engine.local_endpoint',return_value=False):
            self.service.start(self.root,{'mode':'ide','prompt':'Память VALUE'})
            event=self.event('approval');self.assertIsInstance(event['diff'],str)
            preview=json.loads(event['diff']);self.assertEqual(preview['kind'],'project_memory');self.assertEqual(preview['model'],'fixture')
            self.assertIn('PRIVATE_VALUE_DECISION',event['diff'])
            self.service.resolve_approval({**event,'decision':'reject'});self.event('task_end');self.service.thread.join(5)
        self.assertTrue(all('PRIVATE_VALUE_DECISION' not in json.dumps(p) for p in self.server.requests))
