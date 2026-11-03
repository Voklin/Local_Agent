"""Kill and restart an actual Core with a streaming, queued or approval-waiting chat."""
import json
import queue
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

import test_bridge_process as fixture


class RestartHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def do_GET(self):
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
        self.wfile.write(b'{"data":[{"id":"fixture"}]}')

    def do_POST(self):
        payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.requests.append(payload)
        prompt=next(m['content'] for m in reversed(payload['messages']) if m['role']=='user' and isinstance(m.get('content'),str))
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        delta={'tool_calls':[{'index':0,'id':'child-call','type':'function','function':{'name':'delegate_readonly','arguments':'{"task":"hold"}'}}]} if prompt=='parent-child' else {'content':'durable alpha fragment'} if prompt=='hold' else {'tool_calls':[{'index':0,'id':'pending-write','type':'function','function':{'name':'write_file','arguments':'{"path":"never.txt","content":"not approved","overwrite":false}'}}]}
        frame={'id':'fixture','choices':[{'index':0,'delta':delta,'finish_reason':None if prompt=='hold' else 'tool_calls'}]}
        self.wfile.write(('data: '+json.dumps(frame)+'\n\n').encode());self.wfile.flush()
        if prompt=='hold':
            self.connection.settimeout(15)
            try:self.connection.recv(1)
            except OSError:pass
        else:self.wfile.write(b'data: [DONE]\n\n');self.wfile.flush()


class RunOwnerRestartTests(unittest.TestCase):
    setUp=fixture.BridgeProcessTests.setUp
    tearDown=fixture.BridgeProcessTests.tearDown
    start_process=fixture.BridgeProcessTests.start_process
    stop_process=fixture.BridgeProcessTests.stop_process
    read_output=fixture.BridgeProcessTests.read_output
    until=fixture.BridgeProcessTests.until
    call=fixture.BridgeProcessTests.call

    def server(self):
        self.scenario_server=server=ThreadingHTTPServer(('127.0.0.1',0),RestartHandler)
        server.requests=[];server.release=threading.Event()
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.assertTrue(self.call('configure_model',base_url=f'http://127.0.0.1:{server.server_port}/v1',model='fixture')['ok'])
        return server

    def restart(self):
        self.stop_process(kill=True)
        self.messages=queue.Queue();self.buffer=[];self.start_process()
        self.assertTrue(self.call('health')['ok'])

    def test_kill_recovers_stream_and_queue_without_http_or_duplicate_fragment(self):
        server=self.server()
        a=self.call('start_task',mode='chat',prompt='hold');self.assertTrue(a['ok'])
        self.until(lambda e:e.get('event')=='text_delta' and e.get('chat_id')==a['chat_id'])
        self.assertTrue(self.call('new_chat',mode='chat')['ok'])
        b=self.call('start_task',mode='chat',prompt='queued');self.assertTrue(b['ok'])
        end=time.monotonic()+5
        while time.monotonic()<end:
            if self.call('run_history',chat_id=b['chat_id'])['runs'][0]['ledger']['queued_requests']:break
            time.sleep(.02)
        else:self.fail('Second request did not queue')
        self.assertEqual(len(server.requests),1)
        self.restart()
        for run in (a,b,a):
            result=self.call('load_chat',mode='chat',chat_id=run['chat_id']);self.assertTrue(result['ok'],result)
            self.assertEqual(result['task']['status'],'paused');self.assertNotIn('active_run',result)
            ledger=result['task']['run_ledger']
            self.assertEqual(ledger['active_reserved_tokens'],0);self.assertEqual(ledger['queued_requests'],0);self.assertEqual(ledger['interrupted'],1)
            history=self.call('run_history',chat_id=run['chat_id'])['runs'][0]
            self.assertTrue(history['recovered']);self.assertEqual(history['recovery_cause'],'owner_exited')
            self.assertTrue(history['owner_token']);self.assertEqual(history['state'],'paused')
            replies=[m['content'] for m in result['chat']['messages'] if m.get('role')=='assistant' and isinstance(m.get('content'),str)]
            self.assertEqual(replies,['durable alpha fragment'] if run==a else [])
        self.assertEqual(self.call('active_runs')['runs'],[]);self.assertEqual(len(server.requests),1)

    def test_kill_invalidates_write_consent_without_replaying_the_action(self):
        server=self.server();self.assertTrue(self.call('set_project',root=str(self.root))['ok'])
        run=self.call('start_task',mode='ide',prompt='write');self.assertTrue(run['ok'])
        approval=self.until(lambda e:e.get('event')=='approval')
        self.assertFalse((self.root/'never.txt').exists())
        self.restart();self.assertTrue(self.call('set_project',root=str(self.root))['ok'])
        result=self.call('load_chat',mode='ide',chat_id=run['chat_id']);self.assertTrue(result['ok'],result)
        self.assertEqual(result['task']['status'],'paused')
        self.assertFalse(self.call('resolve_approval',run_id=approval['run_id'],approval_id=approval['approval_id'],decision='apply')['ok'])
        self.assertFalse((self.root/'never.txt').exists());self.assertEqual(len(server.requests),1)
        self.assertTrue(self.call('run_history',chat_id=run['chat_id'])['runs'][0]['recovered'])

    def test_kill_recovers_parent_child_tree_without_restarting_child(self):
        server=self.server();self.assertTrue(self.call('set_project',root=str(self.root))['ok'])
        run=self.call('start_task',mode='ide',prompt='parent-child');self.assertTrue(run['ok'])
        end=time.monotonic()+8
        while time.monotonic()<end:
            history=self.call('run_history',chat_id=run['chat_id'])['runs']
            if len(history)==2 and sum(r['ledger']['http_attempts'] for r in history)==2:break
            time.sleep(.03)
        else:self.fail('Child did not acquire its own HTTP lease')
        self.restart();self.assertTrue(self.call('set_project',root=str(self.root))['ok'])
        result=self.call('load_chat',mode='ide',chat_id=run['chat_id']);self.assertTrue(result['ok'],result)
        self.assertEqual(result['task']['run_state'],'paused')
        self.assertEqual(result['task']['children'][0]['state'],'paused')
        history=self.call('run_history',chat_id=run['chat_id'])['runs']
        self.assertEqual(len(history),2);self.assertTrue(all(r['recovered'] for r in history))
        self.assertTrue(all(r['ledger']['active_reserved_tokens']==0 for r in history))
        self.assertEqual(len(server.requests),2);self.assertEqual(self.call('active_runs')['runs'],[])
