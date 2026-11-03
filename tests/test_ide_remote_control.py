"""Native IDE remote control uses an ephemeral view; no Telegram traffic is sent."""
from contextvars import ContextVar
from pathlib import Path
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
from core.python.ide_sessions import IdeSessions,IDE_ROOT
from core.python.task_service import TaskService
from core.python.telegram_service import TelegramService


class IdeRemoteControlTests(unittest.TestCase):
    def owner(self):
        owner=TaskService.__new__(TaskService);owner.lock=threading.RLock();owner.view_session=ContextVar('test_session',default=None);owner.view_adapter=ContextVar('test_adapter',default=None)
        owner.main_sessions=SimpleNamespace(chat={'id':'desktop','mode':'chat'},project_id='');owner.workspace_adapters={};owner.config={'model':'fixture'}
        run=SimpleNamespace(workspace_adapter=SimpleNamespace(identity='view'),chat={'id':'native','mode':'ide'},project_id='',task_running=True,run_id='run-native',approval='approve-native',approval_event={'approval_id':'approve-native','kind':'write','path':'main.ts','diff':'diff'},engine=SimpleNamespace(task_snapshot=lambda:{'status':'running'}),resolve_approval=Mock(return_value={'ok':True}))
        owner.runs={'native':run};views=IdeSessions(owner,Mock());views.views={'view':{'root':Path('C:/native-project')}}
        return owner,run,views

    def test_remote_owner_controls_native_run_without_switching_desktop(self):
        owner,run,views=self.owner();bot=TelegramService(owner,lambda:IDE_ROOT.get(),Mock(),Mock(),views.control);bot.owner=123;bot.send=Mock()
        def command(text):bot.command({'from':{'id':123},'chat':{'id':123,'type':'private'},'text':text})
        command('/status');self.assertIn('native-project',bot.send.call_args.args[0]);self.assertEqual(bot.remote_chat,'native')
        command('/approve approve-native');run.resolve_approval.assert_called_once_with({'run_id':'run-native','approval_id':'approve-native','decision':'apply'})
        self.assertEqual(owner.chat['id'],'desktop');self.assertIsNone(owner.view_session.get());self.assertIsNone(IDE_ROOT.get())

    def test_ambiguous_native_runs_are_not_silently_selected(self):
        owner,run,views=self.owner();owner.runs['another']=SimpleNamespace(task_running=True,workspace_adapter=SimpleNamespace(identity='other'))
        with views.control(None) as selected:self.assertIsNone(selected)
        self.assertEqual(owner.chat['id'],'desktop')
        with views.control('native') as selected:self.assertIs(selected,run);self.assertEqual(owner.chat['id'],'native')
        self.assertEqual(owner.chat['id'],'desktop')
