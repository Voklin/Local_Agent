"""Tiny real stdio LSP server for diagnostics, foreign URI and denied edits tests."""
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.language_diagnostics import read_frame,write_frame


def main():
    if '--stall' in sys.argv:time.sleep(30);return
    uri=''
    while True:
        message=read_frame(sys.stdin.buffer);method=message.get('method')
        if method=='initialize':write_frame(sys.stdout.buffer,{'id':message['id'],'result':{'capabilities':{'textDocumentSync':1,**({'diagnosticProvider':{'interFileDependencies':False,'workspaceDiagnostics':False}} if '--pull' in sys.argv else {})}}})
        elif method=='textDocument/didOpen':
            uri=message['params']['textDocument']['uri']
            if '--late' in sys.argv or '--pull' in sys.argv:
                write_frame(sys.stdout.buffer,{'method':'textDocument/publishDiagnostics','params':{'uri':uri,'version':1,'diagnostics':[]}})
                if '--late' in sys.argv:
                    time.sleep(.2)
                    write_frame(sys.stdout.buffer,{'method':'textDocument/publishDiagnostics','params':{'uri':uri,'version':1,'diagnostics':[{'range':{'start':{'line':0,'character':0}},'message':'Delayed fixture error'}]}})
                continue
            write_frame(sys.stdout.buffer,{'method':'textDocument/publishDiagnostics','params':{'uri':uri+'-foreign','diagnostics':[]}})
            write_frame(sys.stdout.buffer,{'id':90,'method':'workspace/applyEdit','params':{'edit':{'changes':{uri:[{'newText':'UNAUTHORIZED'}]}}}})
        elif message.get('id')==90:
            if message.get('error',{}).get('code')!=-32601:raise RuntimeError('Client must refuse edit requests')
            write_frame(sys.stdout.buffer,{'method':'textDocument/publishDiagnostics','params':{'uri':uri,'version':1,'diagnostics':[{'range':{'start':{'line':1,'character':2},'end':{'line':1,'character':3}},'severity':2,'message':'Fixture warning','source':'fixture-lsp'}]}})
        elif method=='textDocument/diagnostic':write_frame(sys.stdout.buffer,{'id':message['id'],'result':{'kind':'full','items':[] if '--clean' in sys.argv else [{'range':{'start':{'line':0,'character':0}},'message':'Delayed fixture error'}]}})
        elif method=='shutdown':write_frame(sys.stdout.buffer,{'id':message['id'],'result':None})
        elif method=='exit':return


if __name__=='__main__':main()
