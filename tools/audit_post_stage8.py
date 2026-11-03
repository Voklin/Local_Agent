"""Read-only post-stage-8 probes using synthetic replies and disposable source files.

These observations describe existing shortcomings; they are not passing regression
assertions. No user project, model server, real credentials or installed app is used.
"""
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from agent import engine as engine_module,task_store
from agent.json_tools import parse_tool_json,JsonToolStream
from agent.language_diagnostics import diagnose
from agent.operation_context import OperationContext
from agent.tools import read_file
from agent.verifier import StageVerifier
from core.python.editor_service import EditorService
from agent.workspace_revision import WorkspaceRevisionService


class SyntheticStream:
    """One controlled assistant chunk with no terminal finish_reason."""
    def __init__(self,text):self.text=text
    def __iter__(self):
        """Return model data without using an HTTP endpoint."""
        yield NS(choices=[NS(delta=NS(content=self.text,tool_calls=[],refusal=None),finish_reason=None)])
    def close(self):
        """Match the cancellable stream interface; no resource is held."""
        pass


def json_probes():
    """Observe trailing-data acceptance and manufactured completion for JSON calls."""
    call=json.dumps({'tool_calls':[{'name':'read_file','arguments':{'path':'example.txt'}}]})
    converted=next(iter(JsonToolStream(SyntheticStream(call),{'read_file'},'auto')))
    def accepted(text):
        """Observe rejection without turning a successful strict-parser guard into a probe crash."""
        try:return bool(parse_tool_json(text,{'read_file'}))
        except ValueError:return False
    return {'trailing_prose_accepted':accepted(call+' This is only an example; do not execute.'),
        'second_json_accepted':accepted(call+' {"final":"example"}'),
        'no_finish_reason_converted_to':converted.choices[0].finish_reason}


def eof_probe(root):
    """Run the real engine with a synthetic EOF and its actual deterministic verifier."""
    class Client:
        """Offline substitute for HTTP only; the engine/verifier remain real."""
        def __init__(self,*args,**kwargs):pass
        def create(self,**params):
            """Produce a text reply that lacks a terminal completion status."""
            return SyntheticStream('Synthetic answer without a completion status')
        def close(self):
            """No background transport is opened by the fixture."""
            pass
        def cancel(self):
            """Satisfy engine cancellation without side effects."""
            pass
    errors=[]
    with patch.object(task_store,'TASK_DIR',root/'tasks'),patch.object(engine_module,'ModelClient',Client):
        engine=engine_module.AgentEngine('http://unused.invalid','','fixture',str(root),'Explain the project',
            task_id='a'*32,auto_memory=False,allow_tools=False,settings={'max_agent_turns':2})
        engine.failed.connect(errors.append);engine.run();state=engine.task_snapshot()
    return {'status':state['status'],'finish_reason':state.get('finish_reason'),'errors':errors}


def edit_evidence_probe(root):
    """Compare a synthetic command receipt with a real manual editor save."""
    target=root/'example.py';target.write_text('print(1)\n',encoding='utf-8')
    task={'project_root':str(root),'workspace_generation':0,'test_results':[]};verifier=StageVerifier()
    verifier.record_command(task,{'program':'python','arguments':['example.py'],'purpose':'synthetic check'},
        {'ok':True,'exit_code':0,'workspace_generation':0,'workspace_revision':WorkspaceRevisionService.capture(root)})
    editor=EditorService();document=editor.read(root,'example.py')
    preview=editor.preview(root,{'path':'example.py','content':'print(2)\n','revision':document['revision']})
    applied=editor.resolve(root,{'proposal_id':preview['proposal_id'],'decision':'apply'})
    return {'receipt_is_fixture':True,'editor_applied':applied['ok'],'status_after_manual_edit':verifier.command_summary(task)['status']}


def lsp_probe(root):
    """Send empty then delayed nonempty publishDiagnostics through a real subprocess."""
    script=root/'empty_first_lsp.py'
    script.write_text('import sys,time\nsys.path.insert(0,'+repr(str(ROOT))+')\n'
        'from agent.language_diagnostics import read_frame,write_frame\n'
        'while True:\n'
        ' m=read_frame(sys.stdin.buffer)\n'
        ' if m.get("method")=="initialize":write_frame(sys.stdout.buffer,{"id":m["id"],"result":{"capabilities":{}}})\n'
        ' elif m.get("method")=="textDocument/didOpen":\n'
        '  uri=m["params"]["textDocument"]["uri"]\n'
        '  write_frame(sys.stdout.buffer,{"method":"textDocument/publishDiagnostics","params":{"uri":uri,"version":1,"diagnostics":[]}})\n'
        '  time.sleep(.2)\n'
        '  write_frame(sys.stdout.buffer,{"method":"textDocument/publishDiagnostics","params":{"uri":uri,"version":1,"diagnostics":[{"range":{"start":{"line":0,"character":0}},"severity":1,"message":"Delayed real diagnostic"}]}})\n'
        ' elif m.get("method")=="exit":break\n',encoding='utf-8')
    settings={'program':sys.executable,'arguments':['-u',str(script)],'language':'python'}
    result=diagnose(root,'example.py',settings,OperationContext(3))
    return {'ok':result['ok'],'returned_diagnostics':len(result['diagnostics']),'fixture_schedules_error_after_empty':True}


def main():
    """Print current observed gaps as JSON without changing production sources or data."""
    with tempfile.TemporaryDirectory(prefix='neutral-post-stage8-audit-') as directory:
        root=Path(directory);observations={'json':json_probes(),'native_eof':eof_probe(root),'manual_editor':edit_evidence_probe(root)}
        (root/'.env').write_text('SYNTHETIC_AUDIT_VALUE=1\n',encoding='utf-8')
        try:readable=read_file(str(root),'.env')['ok']
        except PermissionError:readable=False
        observations['sensitive_path']={'synthetic_env_readable':readable}
        observations['lsp']=lsp_probe(root)
        print(json.dumps(observations,ensure_ascii=True,indent=2))


if __name__=='__main__':main()
