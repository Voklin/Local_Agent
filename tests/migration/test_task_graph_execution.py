"""A multi-file graph across context compaction, approvals and a real Core restart."""
import json
import queue
import sys
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from tests.migration import test_run_control as fixture
import test_bridge_process as bridge_fixture

CONTENT_A='value_a = 1\n'*900
CONTENT_B='value_b = 2\n'*900
CHECK_ARGS=['-c',"from pathlib import Path; assert 'value_a' in Path('a.py').read_text(); assert 'value_b' in Path('b.py').read_text(); print('ok')"]


def options(fail=False):
    return {'checks':[{'id':'both','purpose':'Оба файла созданы','program':sys.executable,'arguments':['-c','raise SystemExit(1)'] if fail else CHECK_ARGS,'cwd':'.','timeout':30,'evidence_scope':{'kind':'files','files':['a.py','b.py'],'dependencies':[]}}]}


class GraphHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):self.send_error(404)

    def do_POST(self):
        payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.requests.append(payload)
        if getattr(self.server,'loop',False):
            delta={'tool_calls':[{'index':0,'id':'loop','type':'function','function':{'name':'read_range','arguments':'{"path":"main.py","start_line":1,"end_line":1}'}}]}
            self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers();self.wfile.write(('data: '+json.dumps({'id':'fixture','choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls'}]})+'\n\ndata: [DONE]\n\n').encode());return
        nodes=[];results=[]
        for message in payload['messages']:
            if message['role']=='system' and 'CURRENT AGENT STATE' in message.get('content',''):
                text=message['content'];start=text.index('[',text.index('CURRENT AGENT STATE'))
                nodes=json.JSONDecoder().raw_decode(text[start:])[0][0].get('plan_steps',[])
            if message['role']=='assistant' and isinstance(message.get('content'),str) and message['content'].startswith(('[Архив контекста','[Сохранённый обмен')):
                try:
                    archived=json.loads(message['content'].split('\n',1)[1]);results.extend(archived.get('tool_evidence',[]))
                    results.extend(json.loads(c['result']) for c in archived.get('calls',[]))
                except (ValueError,KeyError,TypeError):pass
            if message['role']=='tool':
                try:results.append(json.loads(message['content']))
                except ValueError:pass
        states={n['id']:n['status'] for n in nodes}
        action=None;identity=''
        if not nodes:
            action=('set_task_plan',{'steps':[{'id':'a','title':'Создать a','kind':'change','depends_on':[],'affected_files':['a.py'],'check_ids':[]},
                {'id':'b','title':'Создать b','kind':'change','depends_on':['a'],'affected_files':['b.py'],'check_ids':[]},
                {'id':'verify','title':'Проверить оба файла','kind':'verification','depends_on':['b'],'affected_files':['a.py','b.py'],'check_ids':['both']}],'criteria':[]});identity='plan'
        else:
            for node,path,content in [('a','a.py',CONTENT_A),('b','b.py',CONTENT_B)]:
                if states.get(node)=='done':continue
                if node=='b' and getattr(self.server,'hold_between',False):
                    self.server.waiting.set();self.connection.settimeout(15)
                    try:self.connection.recv(1)
                    except OSError:pass
                    return
                write=next((r for r in reversed(results) if r.get('ok') and r.get('path')==path and 'bytes_written' in r),None)
                action=('update_task_step',{'id':node,'status':'done','evidence':[write['_receipt']]}) if write else ('write_file',{'path':path,'content':content,'overwrite':False})
                identity=node+'_done' if write else node+'_write';break
            if not action and states.get('verify')!='done':
                command=next((r for r in reversed(results) if 'exit_code' in r),None)
                if command and command.get('exit_code')!=0:action=None;identity='failed-final'
                elif command:action=('update_task_step',{'id':'verify','status':'done','evidence':[command['_receipt']]});identity='verify_done'
                else:action=('run_project_command',{k:v for k,v in options(getattr(self.server,'fail',False))['checks'][0].items() if k in ('program','arguments','cwd','timeout')}|{'check_id':'both'});identity='check'
        if action:
            name,args=action;self.server.actions.append(name+':'+identity)
            delta={'tool_calls':[{'index':0,'id':identity,'type':'function','function':{'name':name,'arguments':json.dumps(args)}}]}
        else:delta={'content':'Оба файла готовы.'}
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        self.wfile.write(('data: '+json.dumps({'id':'fixture','choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if action else 'stop'}]})+'\n\ndata: [DONE]\n\n').encode());self.wfile.flush()


class GraphExecutionTests(unittest.TestCase):
    setUp=fixture.RunControlHttpTests.setUp
    stop_server=fixture.RunControlHttpTests.stop_server

    def run_graph(self,fail=False):
        self.server.RequestHandlerClass=GraphHandler;self.server.fail=fail;self.server.actions=[]
        self.service.configure({**self.service.config,'tool_protocol':'native','settings':{'budget_mode':'manual','context_window':32768,'max_tokens':1024,'max_context_chars':20000,'memory_updates':'off'}})
        self.service.extensions.state['groups']['commands']=True
        self.service.start(self.root,{'mode':'ide','prompt':'graph','task_options':options(fail)})
        events=[]
        while True:
            event=self.events.get(timeout=15);events.append(event)
            if event['event']=='approval':self.service.resolve_approval({**event,'decision':'apply'})
            if event['event']=='task_end':break
        from pathlib import Path
        report=Path(__file__).resolve().parents[2]/'.test-data/graph-debug.json'
        report.write_text(json.dumps({'task':self.service.chat['task_checkpoint'],'messages':self.service.chat['messages'],'actions':self.server.actions,'requests':self.server.requests},ensure_ascii=False),encoding='utf-8')
        return self.service.chat['task_checkpoint'],events

    def test_multi_file_graph_completes_with_scoped_checks_after_compaction(self):
        task,events=self.run_graph()
        self.assertEqual(task['status'],'completed',task.get('stop_reason'))
        self.assertEqual([n['status'] for n in task['plan_steps']],['done']*3)
        self.assertEqual((self.root/'a.py').read_text(),CONTENT_A);self.assertEqual((self.root/'b.py').read_text(),CONTENT_B)
        self.assertEqual(task['verification']['status'],'scoped_passed')
        self.assertTrue(any(e.get('task',{}).get('context',{}).get('compressed') for e in events))
        self.assertEqual(len([e for e in events if e['event']=='approval']),3)

    def test_failed_check_cannot_be_hidden_by_final_text(self):
        task,_=self.run_graph(fail=True)
        self.assertEqual(task['status'],'paused');self.assertEqual(task['verification']['status'],'failed')
        self.assertNotEqual(task['plan_steps'][-1]['status'],'done')

    def test_repeated_results_get_one_diagnostic_then_pause(self):
        (self.root/'main.py').write_text('value=1\n');self.server.loop=True
        task,_=self.run_graph()
        self.assertEqual(task['status'],'paused')
        self.assertEqual(task['progress_watchdog']['recovery_attempts'],1)
        diagnostic=sum(any(m.get('role')=='user' and 'HOST PROGRESS CONTROL' in str(m.get('content')) for m in r['messages']) for r in self.server.requests)
        self.assertEqual(diagnostic,1);self.assertLessEqual(len(self.server.requests),6)


class GraphRestartTests(unittest.TestCase):
    setUp=bridge_fixture.BridgeProcessTests.setUp
    tearDown=bridge_fixture.BridgeProcessTests.tearDown
    start_process=bridge_fixture.BridgeProcessTests.start_process
    stop_process=bridge_fixture.BridgeProcessTests.stop_process
    read_output=bridge_fixture.BridgeProcessTests.read_output
    until=bridge_fixture.BridgeProcessTests.until
    call=bridge_fixture.BridgeProcessTests.call

    def advance(self,waiting=False):
        end=time.monotonic()+25
        while time.monotonic()<end:
            if waiting and self.scenario_server.waiting.is_set():return
            try:event=self.messages.get(timeout=.05)
            except queue.Empty:continue
            if event.get('event')=='approval':self.assertTrue(self.call('resolve_approval',run_id=event['run_id'],approval_id=event['approval_id'],decision='apply')['ok'])
            if event.get('event')=='task_end' and not waiting:return
            if event.get('event')=='failed':self.fail(event['text'])
        self.fail('Graph progress timeout')

    def test_real_restart_preserves_completed_node_and_never_replays_its_write(self):
        server=self.scenario_server=ThreadingHTTPServer(('127.0.0.1',0),GraphHandler)
        server.requests=[];server.actions=[];server.hold_between=True;server.waiting=threading.Event();server.release=threading.Event()
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.assertTrue(self.call('set_project',root=str(self.root))['ok'])
        self.assertTrue(self.call('extensions_configure',kind='groups',id='commands',enabled=True)['ok'])
        self.assertTrue(self.call('configure_model',base_url=f'http://127.0.0.1:{server.server_port}/v1',model='fixture',settings={'budget_mode':'manual','context_window':32768,'max_tokens':1024,'max_context_chars':20000,'memory_updates':'off'})['ok'])
        started=self.call('start_task',mode='ide',prompt='graph',task_options=options());self.assertTrue(started['ok'])
        self.advance(waiting=True)
        self.assertTrue((self.root/'a.py').exists());self.assertFalse((self.root/'b.py').exists())
        self.stop_process(kill=True);self.messages=queue.Queue();self.buffer=[];self.start_process();server.hold_between=False
        self.assertTrue(self.call('set_project',root=str(self.root))['ok'])
        recovered=self.call('load_chat',mode='ide',chat_id=started['chat_id']);self.assertTrue(recovered['ok'])
        self.assertEqual(recovered['task']['plan_steps'][0]['status'],'done')
        self.assertTrue(self.call('start_task',mode='ide',resume=True)['ok']);self.advance()
        final=self.call('load_chat',mode='ide',chat_id=started['chat_id'])['task']
        self.assertEqual(final['status'],'completed',final.get('stop_reason'))
        self.assertEqual(server.actions.count('write_file:a_write'),1)
        self.assertEqual([n['status'] for n in final['plan_steps']],['done']*3)
