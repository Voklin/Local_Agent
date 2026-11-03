import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from core.python.assistant_service import AssistantService,calculate
from core.python.desktop_service import DesktopService,music_url


class AssistantTests(unittest.TestCase):
    def test_calculator_has_no_calls_names_or_unbounded_powers(self):
        self.assertEqual(calculate('(125*8)+20/4'),1005)
        for expression in ("__import__('os').system('x')",'2**9999','[1,2]','float("inf")'):
            with self.assertRaises((ValueError,SyntaxError)):calculate(expression)

    def test_notes_persist_without_arbitrary_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            service=AssistantService(lambda e:None);service.notes_file=Path(directory)/'notes.json'
            service.execute('save_note',{'text':'Купить чай','title':'Покупки'})
            again=AssistantService(lambda e:None);again.notes_file=service.notes_file
            self.assertEqual(again.execute('list_notes',{'query':'чай'})['total'],1)
            service.notes_file.write_text('broken')
            with self.assertRaises(ValueError):service.execute('save_note',{'text':'Новая'})
            self.assertEqual(service.notes_file.read_text(),'broken');service.shutdown();again.shutdown()

    def test_timer_emits_once_and_cancelled_timer_does_not_fire(self):
        events=[];service=AssistantService(events.append)
        timer=service.execute('set_timer',{'seconds':60,'label':'Чай'})['timer']
        service.fire(timer['id']);service.fire(timer['id']);self.assertEqual(len(events),1)
        second=service.execute('set_timer',{'seconds':60})['timer'];service.execute('cancel_timer',{'id':second['id']});service.fire(second['id'])
        self.assertEqual(len(events),1);service.shutdown();self.assertEqual(service.timers,{})

    def test_full_unicode_notes_capacity_stays_readable_after_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            service=AssistantService(lambda e:None);service.notes_file=Path(directory)/'notes.json'
            text='я'*4000
            values=[{'id':str(index),'title':'Заметка','text':text} for index in range(199)]
            service.notes_file.write_text(json.dumps(values,ensure_ascii=False,indent=2),encoding='utf-8')
            self.assertTrue(service.execute('save_note',{'text':text})['ok'])
            again=AssistantService(lambda e:None);again.notes_file=service.notes_file
            self.assertEqual(again.execute('list_notes',{})['total'],200)
            previous=service.notes_file.read_bytes()
            with self.assertRaises(ValueError):service.execute('save_note',{'text':'201'})
            self.assertEqual(service.notes_file.read_bytes(),previous)
            service.shutdown();again.shutdown()

    def test_note_limit_counts_whitespace_without_corrupting_store(self):
        with tempfile.TemporaryDirectory() as directory:
            service=AssistantService(lambda e:None);service.notes_file=Path(directory)/'notes.json'
            service.execute('save_note',{'text':'Исходная заметка'})
            previous=service.notes_file.read_bytes()
            with self.assertRaises(ValueError):service.execute('save_note',{'text':'x'+' '*4000})
            self.assertEqual(service.notes_file.read_bytes(),previous)
            service.shutdown()

    def test_music_links_reject_executables_private_hosts_and_spoofing(self):
        self.assertEqual(music_url('https://www.youtube.com/watch?v=abc'),'https://www.youtube.com/watch?v=abc')
        for value in ('file:///C:/x.exe','https://localhost/a','https://youtube.com.evil/a','https://user:pass@youtube.com/a','https://youtube.com:444/a'):
            with self.assertRaises(ValueError):music_url(value)

    def test_music_search_encodes_query_and_does_not_claim_playback(self):
        with patch('core.python.desktop_service.search_web',return_value={'ok':True,'results':[]}):
            service=DesktopService(lambda e:None);service.enabled=True;calls=[]
            with patch.object(service,'request',side_effect=lambda op,args,cancel:(calls.append((op,args)) or {'ok':True})):
                result=service.execute('music_search',{'query':'a & b','service':'youtube'},'Найди музыку',threading.Event())
            self.assertFalse(result['playback_confirmed']);self.assertTrue(result['browser_opened']);self.assertIn('a%20%26%20b',calls[0][1]['url'])

    def test_local_audio_requires_original_prompt_folder_and_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);song=root/'song.mp3';song.write_bytes(b'fixture');exe=root/'script.exe';exe.write_bytes(b'fixture')
            service=DesktopService(lambda e:None);service.enabled=True
            with patch.object(service,'request',return_value={'ok':True}) as host:
                self.assertFalse(service.execute('play_local_audio',{'path':str(song)},'Включи музыку',threading.Event())['ok'])
                self.assertTrue(service.execute('play_local_audio',{'path':str(song)},f'Включи из "{root}"',threading.Event())['ok'])
                self.assertFalse(service.execute('play_local_audio',{'path':str(exe)},f'Включи из "{root}"',threading.Event())['ok'])
                self.assertEqual(host.call_count,1)


if __name__=='__main__':unittest.main()
