"""Two real engine workers, one HTTP lease, isolated streams and approvals."""
import json
import threading
import time
import unittest

from agent import chat_store
from tests.migration import test_run_control as fixture


class BackgroundRunTests(unittest.TestCase):
    setUp=fixture.RunControlHttpTests.setUp
    stop_server=fixture.RunControlHttpTests.stop_server

    def install_handler(self):
        from http.server import BaseHTTPRequestHandler
        server=self.server
        server.release=threading.Event();self.addCleanup(server.release.set)
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass

            def do_GET(self):
                self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
                self.wfile.write(b'{"data":[{"id":"fixture"}]}')

            def do_POST(self):
                payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])));server.requests.append(payload)
                if not payload.get('stream'):
                    self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
                    self.wfile.write(json.dumps({'id':'fixture','choices':[{'index':0,'message':{'role':'assistant','content':'{}'},'finish_reason':'stop'}]}).encode())
                    return
                user=next(m['content'] for m in payload['messages'] if m['role']=='user' and isinstance(m.get('content'),str) and m['content'].startswith(('hold-alpha','beta','write-')))
                self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
                try:
                    if user.startswith('write-') and not any(m.get('role')=='tool' for m in payload['messages']):
                        delta={'tool_calls':[{'index':0,'id':'same-id','type':'function','function':{'name':'write_file','arguments':json.dumps({'path':'new.txt','content':user,'overwrite':False})}}]}
                    else:delta={'content':'alpha-part' if user=='hold-alpha' else user+' done'}
                    self.wfile.write(('data: '+json.dumps({'id':'fixture','choices':[{'index':0,'delta':delta,'finish_reason':None}]})+'\n\n').encode());self.wfile.flush()
                    if user=='hold-alpha':server.release.wait(15)
                    self.wfile.write(('data: '+json.dumps({'id':'fixture','choices':[{'index':0,'delta':{},'finish_reason':'tool_calls' if 'tool_calls' in delta else 'stop'}]})+'\n\ndata: [DONE]\n\n').encode());self.wfile.flush()
                except (BrokenPipeError,ConnectionResetError):pass
        server.RequestHandlerClass=Handler
        self.service.config['tool_protocol']='native'

    def event(self,name,chat_id=None):
        end=time.monotonic()+12
        while time.monotonic()<end:
            value=self.events.get(timeout=max(.01,end-time.monotonic()))
            if value['event']=='failed':self.fail(value['text'])
            if value['event']==name and (chat_id is None or value['chat_id']==chat_id):return value
        self.fail('Event not received: '+name)

    def wait_queued(self,run):
        end=time.monotonic()+5
        while time.monotonic()<end:
            if self.service.registry.snapshot(run['run_id'])['ledger']['queued_requests']:return
            time.sleep(.02)
        self.fail('Second request did not enter the scheduler queue')

    def test_switch_and_cancel_queued_chat_preserve_other_live_stream(self):
        self.install_handler()
        a=self.service.start('',{'prompt':'hold-alpha','mode':'chat'});self.event('text_delta',a['chat_id'])
        a_worker=self.service.selected_run()
        b_chat=self.service.select_chat('',mode='chat')['chat']['id']
        b=self.service.start('',{'prompt':'beta','mode':'chat'});self.wait_queued(b)
        live=self.service.select_chat('',a['chat_id'],'chat')
        self.assertEqual(live['active_run']['run_id'],a['run_id'])
        self.assertEqual(live['task']['status'],'running')
        fragment=live['chat']['messages'][-1]
        self.assertEqual(fragment['content'],'alpha-part');self.assertTrue(fragment['streaming'])
        self.assertTrue(fragment['message_id'].startswith(a['run_id']))
        self.assertGreaterEqual(live['event_seq'],1)
        self.assertEqual(chat_store.load_chat(a['chat_id'])['messages'][-1]['role'],'user')
        with self.assertRaises(ValueError):self.service.cancel({'run_id':b['run_id']})
        with self.assertRaises(ValueError):self.service.start('',{'prompt':'duplicate','mode':'chat'})
        self.service.select_chat('',b_chat,'chat');b_worker=self.service.selected_run()
        self.service.cancel({'run_id':b['run_id']});b_worker.thread.join(5)
        self.assertFalse(b_worker.task_running);self.assertTrue(a_worker.task_running)
        self.assertEqual(self.service.registry.snapshot(b['run_id'])['ledger']['http_attempts'],0)
        self.server.release.set();a_worker.thread.join(5)
        self.assertFalse(a_worker.task_running)
        self.assertEqual(self.service.active_runs(),[])
        saved_a=chat_store.load_chat(a['chat_id']);saved_b=chat_store.load_chat(b_chat)
        self.assertEqual(saved_a['messages'][-1]['content'],'alpha-part')
        self.assertNotIn('alpha-part',json.dumps(saved_b))
        self.assertNotIn('beta',json.dumps(saved_a))
        self.assertEqual(saved_b['task_checkpoint']['status'],'paused')
        self.assertEqual(len(self.server.requests),1)

    def test_two_approvals_are_scoped_and_same_workspace_has_one_writer(self):
        self.install_handler()
        a=self.service.start(self.root,{'prompt':'write-first','mode':'ide'});approval_a=self.event('approval',a['chat_id'])
        self.service.select_chat(self.root,mode='ide')
        with self.assertRaisesRegex(ValueError,'папке уже работает'):self.service.start(self.root,{'prompt':'write-collision','mode':'ide'})
        nested=self.root/'nested';nested.mkdir();self.service.select_chat(nested,mode='ide')
        with self.assertRaisesRegex(ValueError,'папке уже работает'):self.service.start(nested,{'prompt':'write-nested','mode':'ide'})
        other=self.root.parent/'other';other.mkdir()
        self.service.select_chat(other,mode='ide')
        b=self.service.start(other,{'prompt':'write-second','mode':'ide'});approval_b=self.event('approval',b['chat_id'])
        with self.assertRaises(ValueError):self.service.resolve_approval({**approval_a,'decision':'apply'})
        self.assertFalse((self.root/'new.txt').exists());self.assertFalse((other/'new.txt').exists())
        b_worker=self.service.selected_run();self.service.cancel({'run_id':b['run_id']});b_worker.thread.join(5)
        view=self.service.select_chat(self.root,a['chat_id'],'ide')
        self.assertEqual(view['approval']['approval_id'],approval_a['approval_id'])
        self.assertNotEqual(approval_a['approval_id'],approval_b['approval_id'])
        self.service.resolve_approval({**approval_a,'decision':'apply'});self.service.thread.join(5)
        self.assertEqual((self.root/'new.txt').read_text(),'write-first')
        self.assertFalse((other/'new.txt').exists())
        self.assertEqual(chat_store.load_chat(a['chat_id'])['task_checkpoint']['status'],'completed')
        self.assertEqual(chat_store.load_chat(b['chat_id'])['task_checkpoint']['status'],'paused')

    def test_shutdown_cancels_all_owners_and_mismatched_models_are_not_started(self):
        self.install_handler()
        self.service.start('',{'prompt':'hold-alpha','mode':'chat'});self.event('text_delta')
        first=self.service.selected_run()
        self.service.select_chat('',mode='chat')
        config=dict(self.service.config);self.service.config={**config,'model':'different'}
        with self.assertRaisesRegex(ValueError,'одно подключение'):self.service.start('',{'prompt':'beta','mode':'chat'})
        self.service.config=config
        b=self.service.start('',{'prompt':'beta','mode':'chat'});self.wait_queued(b);second=self.service.selected_run()
        self.service.shutdown();self.server.release.set()
        first.thread.join(3);second.thread.join(3)
        self.assertFalse(first.thread.is_alive());self.assertFalse(second.thread.is_alive())
        self.assertEqual(self.service.active_runs(),[])
        self.assertFalse(self.service.scheduler.status()['busy'])
        with self.assertRaises(ValueError):self.service.start('',{'prompt':'beta','mode':'chat'})
