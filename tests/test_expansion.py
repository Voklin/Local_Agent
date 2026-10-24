"""Behavioral contracts for isolated companion, JSON tools, PC grants and Telegram."""
import base64
from copy import deepcopy
import io
import json
from pathlib import Path
import queue
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import wave
import httpx

from agent import chat_store, task_store, companion_preferences
from agent.json_tools import parse_tool_json, prepare_json_request, JsonToolStream
from core.python.task_service import TaskService
from core.python.desktop_service import DesktopService, prompt_folders, search_web
from core.python.telegram_service import TelegramService
from core.python.runtime_service import RuntimeService
from core.python.transcription_service import TranscriptionService


class ExpansionTests(unittest.TestCase):
    def test_lola_wake_migration_preserves_custom_phrase(self):
        self.assertEqual(companion_preferences.validate_profile({**companion_preferences.DEFAULT_PROFILE,'wake_phrase':'Привет, Мия'})['wake_phrase'],'Привет, Лола')
        self.assertEqual(companion_preferences.validate_profile({**companion_preferences.DEFAULT_PROFILE,'wake_phrase':'Доброе утро'})['wake_phrase'],'Доброе утро')

    def test_search_falls_back_to_bing_and_rejects_non_web_links(self):
        requests=[]
        def search_transport(request):
            requests.append(request.url.host)
            if request.url.host=='html.duckduckgo.com':raise httpx.ConnectTimeout('fixture')
            return httpx.Response(200,content=b'<rss><channel><item><title>Test query result</title><link>https://example.org/page</link><description>Snippet</description></item><item><title>Blocked</title><link>file:///C:/private.txt</link></item><item><title>Unrelated</title><link>https://example.org/unrelated</link></item></channel></rss>')
        client=httpx.Client
        with patch('core.python.desktop_service.httpx.Client',side_effect=lambda **kwargs:client(transport=httpx.MockTransport(search_transport),**kwargs)):
            result=search_web('test query',threading.Event())
        self.assertTrue(result['ok']);self.assertEqual(result['provider'],'Bing')
        self.assertEqual(requests,['html.duckduckgo.com','www.bing.com'])
        self.assertEqual(result['results'],[{'title':'Test query result','url':'https://example.org/page','snippet':'Snippet'}])

    def test_application_tools_broker_ids_without_shell_or_arguments(self):
        service=DesktopService(lambda event:None);service.enabled=True
        service.request=Mock(return_value={'ok':True});cancelled=threading.Event()
        self.assertTrue(service.execute('list_applications',{},'Открой блокнот',cancelled)['ok'])
        service.request.assert_called_with('list_applications',{},cancelled)
        self.assertTrue(service.execute('open_application',{'app_id':'notepad'},'Открой блокнот',cancelled)['ok'])
        service.request.assert_called_with('open_application',{'app_id':'notepad'},cancelled)
        service.request.reset_mock()
        for args in ({'app_id':'C:\\Windows\\cmd.exe'},{'app_id':'notepad','args':['file.txt']},{'app_id':'cmd /c test'}):
            self.assertFalse(service.execute('open_application',args,'Открой блокнот',cancelled)['ok'])
        service.request.assert_not_called()
        cancelled.set();self.assertFalse(service.execute('open_application',{'app_id':'notepad'},'',cancelled)['ok'])
        service.enabled=False
        self.assertFalse(service.execute('list_applications',{},'',threading.Event())['ok'])
        service.request.assert_not_called()

    def test_companion_scope_rejects_cross_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch.object(chat_store,'CHAT_DIR',root/'chats'), patch.object(chat_store,'INDEX_FILE',root/'chats/index.json'), patch.object(task_store,'TASK_DIR',root/'tasks'):
                service=TaskService(lambda event:None)
                chat=service.select_chat('',mode='chat')['chat']
                miya=service.select_chat('',mode='voice')['chat']
                self.assertEqual([item['id'] for item in service.chats('','chat')['chats']],[chat['id']])
                self.assertEqual([item['id'] for item in service.chats('','voice')['chats']],[miya['id']])
                with self.assertRaises(ValueError):service.select_chat('',miya['id'],'chat')
                with self.assertRaises(ValueError):service.rename('',{'chat_id':miya['id'],'mode':'chat','title':'x'})
                service.shutdown()

    def test_profile_does_not_persist_keys_or_change_main_model(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(companion_preferences,'PROFILE_FILE',Path(directory)/'miya.json'):
            profile=companion_preferences.save_profile({**companion_preferences.DEFAULT_PROFILE,'model':'small','api_key':'SECRET','stt_api_key':'STT_SECRET','persona':'Терпеливая'})
            self.assertEqual(companion_preferences.load_profile()['model'],'small')
            self.assertEqual(profile['persona'],'Терпеливая')
            self.assertNotIn('SECRET',companion_preferences.PROFILE_FILE.read_text('utf-8'))
            self.assertNotIn('api_key',profile)

    def test_json_tools_never_execute_embedded_examples(self):
        envelope='{"tool_calls":[{"name":"read_file","arguments":{"path":"a.txt"}}]}'
        self.assertEqual(parse_tool_json(envelope,{'read_file'})[0]['function']['name'],'read_file')
        self.assertEqual(parse_tool_json('Example: '+envelope,{'read_file'}),[])
        self.assertEqual(len(parse_tool_json(envelope+'\nКомментарий после JSON',{'read_file'})),1)
        with self.assertRaises(ValueError):parse_tool_json(envelope,{'write_file'})
        with self.assertRaises(ValueError):parse_tool_json('{"tool_calls":[]}',{'read_file'})

    def test_json_request_has_no_native_roles_or_api_fields(self):
        request,allowed,choice=prepare_json_request({'stream':True,'tools':[{'function':{'name':'read_file'}}],'tool_choice':'auto','messages':[
            {'role':'assistant','content':None,'tool_calls':[{'function':{'name':'read_file','arguments':'{"path":"a"}'}}]},
            {'role':'tool','tool_call_id':'id','content':'untrusted'}]})
        self.assertNotIn('tools',request);self.assertNotIn('tool_choice',request)
        self.assertEqual(allowed,{'read_file'});self.assertEqual(choice,'auto')
        self.assertTrue(all(message['role']!='tool' for message in request['messages']))
        self.assertIn('untrusted',request['messages'][-1]['content'])
        from agent.delegation import DELEGATE_TOOL
        miya,allowed,_=prepare_json_request({'tools':[DELEGATE_TOOL],'messages':[{'role':'user','content':'Вопрос'}]})
        self.assertEqual(allowed,{'delegate_task'})
        self.assertIn('delegate_task',miya['messages'][0]['content'])
        self.assertNotIn('read_file',miya['messages'][0]['content'])

    def test_json_stream_converts_complete_reply_to_tool_delta(self):
        chunks=[SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=text))]) for text in ('{"tool":"read_', 'file","arguments":{"path":"a"}}')]
        result=list(JsonToolStream(chunks,{'read_file'},'auto'))
        self.assertEqual(result[0].choices[0].delta.tool_calls[0].function.name,'read_file')
        self.assertIsNone(result[0].choices[0].delta.content)

    def test_pc_folders_come_only_from_human_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);allowed=root/'allowed';allowed.mkdir();outside=root/'outside';outside.mkdir()
            (allowed/'a.txt').write_text('allowed',encoding='utf-8');(outside/'x.txt').write_text('private',encoding='utf-8')
            service=DesktopService(lambda event:None);service.enabled=True
            prompt=f'Посмотри папку "{allowed}"'
            self.assertEqual(prompt_folders(prompt),[allowed.resolve()])
            self.assertTrue(service.execute('read_allowed_file',{'path':str(allowed/'a.txt')},prompt,threading.Event())['ok'])
            self.assertFalse(service.execute('read_allowed_file',{'path':str(outside/'x.txt')},prompt,threading.Event())['ok'])
            self.assertFalse(service.execute('desktop_screenshot',{},prompt,threading.Event())['ok'])
            self.assertFalse(service.execute('desktop_screenshot',{},'Не делай скриншот',threading.Event())['ok'])

    def test_telegram_ignores_other_users_groups_and_forwards(self):
        tasks=SimpleNamespace(lock=threading.RLock(),cancel=Mock())
        service=TelegramService(tasks,lambda:None,lambda event:None,Mock());service.owner=42;service.send=Mock()
        valid={'from':{'id':42},'chat':{'id':42,'type':'private'},'text':'/stop'}
        for message in ({**valid,'from':{'id':43}}, {**valid,'chat':{'id':42,'type':'group'}}, {**valid,'forward_origin':{'type':'user'}}):service.command(message)
        tasks.cancel.assert_not_called();service.send.assert_not_called()
        service.command(valid);tasks.cancel.assert_called_once()

    def test_telegram_approval_keeps_exact_current_id(self):
        tasks=SimpleNamespace(run_id='run',resolve_approval=Mock(),lock=threading.RLock())
        service=TelegramService(tasks,lambda:None,lambda event:None,Mock())
        service.dispatch('/approve','precise-id')
        tasks.resolve_approval.assert_called_once_with({'run_id':'run','approval_id':'precise-id','decision':'apply'})
        self.assertNotIn('token',service.status())
        service.state='connected';service.remote_chat='voice-source'
        service.observe({'event':'handoff_started','source_chat':'voice-source','target_chat':'main-target'})
        self.assertEqual(service.remote_chat,'main-target')
        service.observe({'event':'result','chat_id':'main-target','text':'delegated result'})
        self.assertEqual(service.notifications.get_nowait()['text'],'delegated result')
        tasks.idle=Mock();tasks.chat={'id':'paused-ide','mode':'ide','messages':[{'role':'assistant','content':'Saved result'}]}
        service.emit=Mock()
        self.assertIn('Saved result',service.dispatch('/result',''))
        service.dispatch('/resume','')
        tasks.idle.assert_called_once()
        service.start_task.assert_called_once_with({'mode':'ide','resume':True})
        self.assertEqual(service.remote_chat,'paused-ide')
        self.assertTrue(service.emit.call_args.args[0]['resume'])

    def test_telegram_poll_drops_backlog_and_never_sends_to_stranger(self):
        tasks=SimpleNamespace(lock=threading.RLock(),engine=None,config={'model':'fixture'},cancel=Mock())
        service=TelegramService(tasks,lambda:None,Mock(),Mock());service.owner=42;service.token='123456:fixture_not_a_real_token'
        requests=[];polls=[]
        def transport(request):
            method=request.url.path.rsplit('/',1)[-1];payload=json.loads(request.content);requests.append((method,payload))
            if method=='getMe':result={'username':'fixture_bot'}
            elif method=='getUpdates':
                polls.append(payload)
                if payload.get('offset')==-1:result=[{'update_id':100,'message':{'text':'/stop','from':{'id':42},'chat':{'id':42,'type':'private'}}}]
                elif len(polls)==2:result=[{'update_id':101,'message':{'text':'/stop','from':{'id':99},'chat':{'id':99,'type':'private'}}},{'update_id':102,'message':{'text':'/status','from':{'id':42},'chat':{'id':42,'type':'private'}}}]
                else:service.stop_event.set();result=[]
            else:result={'message_id':1}
            return httpx.Response(200,json={'ok':True,'result':result})
        client=httpx.Client(transport=httpx.MockTransport(transport))
        with patch('core.python.telegram_service.httpx.Client',return_value=client):service.poll()
        tasks.cancel.assert_not_called()
        sent=[payload for method,payload in requests if method=='sendMessage']
        self.assertEqual(len(sent),1);self.assertEqual(sent[0]['chat_id'],42)
        self.assertEqual(sent[0]['link_preview_options'],{'is_disabled':True})
        self.assertEqual(polls[1]['offset'],101);self.assertEqual(service.token,'')

    def test_cache_preferences_survive_new_service(self):
        import core.python.runtime_service as module
        with tempfile.TemporaryDirectory() as directory, patch.object(module,'APP_DIR',Path(directory)):
            root=Path(directory);exe=root/'llama-server.exe';exe.write_bytes(b'fixture');model=root/'fixture.gguf';model.write_bytes(b'GGUF1234')
            service=RuntimeService()
            with patch.object(service.runtime,'start'):
                service.start({'runtime_path':str(exe),'model_path':str(model),'cache_type_k':'q8_0','cache_type_v':'q4_0','threads':3})
                service.thread.join(2)
            reopened=RuntimeService()
            self.assertEqual(reopened.cache_types,{'cache_type_k':'q8_0','cache_type_v':'q4_0'})
            self.assertEqual(reopened.options['threads'],3)
            self.assertNotIn('model_path',json.loads(service.preferences_file.read_text('utf-8')))
            service.shutdown();reopened.shutdown()

    def test_kv_cache_validates_before_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);exe=root/'llama-server.exe';exe.write_bytes(b'fixture');model=root/'a.gguf';model.write_bytes(b'GGUF1234')
            service=RuntimeService()
            with self.assertRaises(ValueError):service.start({'runtime_path':str(exe),'model_path':str(model),'cache_type_k':'--evil'})
            with patch.object(service.runtime,'start') as launch:
                service.start({'runtime_path':str(exe),'model_path':str(model),'cache_type_k':'q8_0','cache_type_v':'q4_0','threads':3})
                service.thread.join(2)
                self.assertEqual(launch.call_args.kwargs['extra_args'],['--threads','3','--parallel','1','--cache-type-k','q8_0','--cache-type-v','q4_0','--flash-attn','on'])
            service.shutdown()

    def test_transcription_rejects_invalid_audio_without_network(self):
        service=TranscriptionService()
        with self.assertRaises(Exception):service.start({'audio':base64.b64encode(b'not audio').decode()}, {}, Mock())
        self.assertIsNone(service.thread)


if __name__=='__main__':unittest.main()
