from copy import deepcopy
import json
import unittest
from agent.smart_context import smart_compact_messages,compact_tool_result


class SmartContextTests(unittest.TestCase):
    def test_archive_uses_serialized_message_size(self):
        messages=[{'role':'system','content':'system '*640},{'role':'user','content':'Inspect all sources'}]
        for index in range(24):messages.extend([
            {'role':'assistant','tool_calls':[{'id':str(index),'type':'function','function':{'name':'read_range','arguments':json.dumps({'path':f'part_{index}.py'})}}]},
            {'role':'tool','tool_call_id':str(index),'content':json.dumps({'ok':True,'path':f'part_{index}.py','sha256':'f'*64,'content':'source line\n'*600})}])
        original=deepcopy(messages)
        result,stats=smart_compact_messages(messages,12000,12,1)
        self.assertLessEqual(len(json.dumps(result,ensure_ascii=False)),12000)
        self.assertGreater(stats['archived_units'],0)
        self.assertEqual(result[0],messages[0]);self.assertIn(messages[1],result)
        self.assertEqual(result[-1]['tool_call_id'],'23')
        self.assertEqual(json.loads(result[-1]['content'])['sha256'],'f'*64)
        self.assertEqual(messages,original)

    def test_graph_receipt_reference_survives_compaction(self):
        receipt={'message_index':8,'call_id':'write-file'}
        raw=json.dumps({'ok':True,'path':'a.py','sha256':'f'*64,'content':'large source '*1000,'_receipt':receipt})
        compacted,_=compact_tool_result(raw,'',900,'write-file',9)
        self.assertEqual(json.loads(compacted)['_receipt'],receipt)
        self.assertEqual(json.loads(compacted)['sha256'],'f'*64)
        self.assertNotEqual(json.loads(compacted)['result_sha256'],'f'*64)
    def test_old_design_constraint_survives_long_history(self):
        messages=[{'role':'system','content':'system'},{'role':'user','content':'Не меняй дизайн. Используй только локальные файлы.'}]
        for index in range(40):messages.extend([{'role':'user','content':f'Вопрос {index}'},{'role':'assistant','content':'Подробный ответ '+str(index)+' x'*100}])
        messages.append({'role':'user','content':'Продолжай'})
        original=deepcopy(messages);projected,stats=smart_compact_messages(messages,4000,4,len(messages)-1)
        self.assertIn('Не меняй дизайн',json.dumps(projected,ensure_ascii=False));self.assertEqual(projected[-1]['content'],'Продолжай')
        self.assertLessEqual(len(json.dumps(projected,ensure_ascii=False)),4000);self.assertTrue(stats['compressed']);self.assertEqual(messages,original)

    def test_tool_pairs_and_write_arguments_are_never_cut(self):
        arguments=json.dumps({'path':'app.py','content':'print(1)\n'*80})
        messages=[{'role':'system','content':'system'},{'role':'user','content':'Создай код'},
          {'role':'assistant','content':None,'tool_calls':[{'id':'write','type':'function','function':{'name':'write_file','arguments':arguments}}]},
          {'role':'tool','tool_call_id':'write','content':json.dumps({'ok':True,'path':'app.py'})}]
        result,_=smart_compact_messages(messages,4000,2,1)
        self.assertEqual(result[-2]['tool_calls'][0]['function']['arguments'],arguments);self.assertEqual(result[-1]['tool_call_id'],'write')

    def test_current_code_handoff_is_protected_or_rejected(self):
        prompt='Полный код:\n'+'def function(): pass\n'*100
        messages=[{'role':'system','content':'system'},{'role':'user','content':prompt}]
        with self.assertRaisesRegex(ValueError,'не обрезан'):smart_compact_messages(messages,600,2,1)
        result,_=smart_compact_messages(messages,6000,2,1);self.assertEqual(result[-1]['content'],prompt)

    def test_large_tool_json_keeps_error_path_and_valid_json(self):
        raw=json.dumps({'ok':True,'path':'app.py','content':'line\n'*5000+'target_function = 42\n'})
        compacted,changed=compact_tool_result(raw,'target_function',1600);value=json.loads(compacted)
        self.assertTrue(changed);self.assertEqual(value['path'],'app.py');self.assertTrue(value['context_compacted'])
        self.assertIn('target_function',value['excerpt']);self.assertIn('sha256',value)

    def test_command_compaction_keeps_exit_code_and_failure_evidence(self):
        output='initial output\n'+'build progress\n'*3000+'FAILED: test_payment_total\n'
        raw=json.dumps({'ok':False,'exit_code':7,'output':output,'stderr':'Traceback: payment total mismatch\n'*400,'elapsed_ms':1500})
        compacted,changed=compact_tool_result(raw,'payment',1800,'call_command')
        value=json.loads(compacted)
        self.assertTrue(changed);self.assertLessEqual(len(compacted),1800)
        self.assertFalse(value['ok']);self.assertEqual(value['exit_code'],7);self.assertEqual(value['elapsed_ms'],1500)
        self.assertIn('test_payment_total',value['output_excerpt']);self.assertIn('Traceback',value['stderr_excerpt'])
        self.assertEqual(value['source_tool_call_id'],'call_command')

    def test_mcp_compaction_keeps_text_blocks_and_excludes_binary_content(self):
        blocks=[{'type':'text','text':'filler\n'*2500+'ERROR: required_mcp_result missing\n'},
                {'type':'image','data':'DO_NOT_INCLUDE_BINARY_PAYLOAD'*500},
                {'type':'text','text':'Other result block'}]
        raw=json.dumps({'ok':False,'content':blocks,'code':'MCP_ERROR'})
        compacted,changed=compact_tool_result(raw,'required_mcp_result',1600,'call_mcp')
        value=json.loads(compacted)
        self.assertTrue(changed);self.assertLessEqual(len(compacted),1600)
        self.assertEqual(value['code'],'MCP_ERROR');self.assertFalse(value['ok'])
        self.assertIn('required_mcp_result',value['content_excerpt'])
        self.assertIn('Other result block',value['content_excerpt'])
        self.assertNotIn('DO_NOT_INCLUDE_BINARY_PAYLOAD',compacted)

    def test_single_line_output_keeps_diagnostic_beyond_prefix(self):
        raw=json.dumps({'ok':False,'exit_code':9,'output':'long_progress_'*3000+' ERROR: target_build_failed'})
        compacted,_=compact_tool_result(raw,'target_build_failed',1200)
        self.assertIn('target_build_failed',json.loads(compacted)['output_excerpt'])

    def test_compacted_json_honors_escaping_budget_and_outcome_metadata(self):
        raw=json.dumps({'ok':False,'exit_code':23,'code':'CHECK_FAILED','status':'failed',
            'error':'Ошибка с кавычками "\\\t\n'*500,'output':'Пример "\\\t\n'*4000,'path':'folder/'+('long_name/'*40)+'main.py'},ensure_ascii=False)
        compacted,_=compact_tool_result(raw,'Ошибка',600,'escaped_call')
        value=json.loads(compacted)
        self.assertLessEqual(len(compacted),600)
        self.assertEqual((value['ok'],value['exit_code'],value['code'],value['status']),(False,23,'CHECK_FAILED','failed'))
        self.assertIn('output_excerpt',value);self.assertIn('error',value)

    def test_compaction_preserves_note_privacy_and_canonical_result_reference(self):
        notes=[{'id':str(index),'title':'Title','content':'PRIVATE_NOTE_TEXT'*500,'created_at':'today'} for index in range(5)]
        compacted,_=compact_tool_result(json.dumps({'ok':True,'notes':notes}),'',1200)
        self.assertNotIn('PRIVATE_NOTE_TEXT',compacted)
        self.assertEqual(json.loads(compacted)['notes_total'],5)
        raw=json.dumps({'ok':False,'exit_code':4,'output':'progress\n'*4000+'FAILED: canonical_test\n'})
        messages=[{'role':'system','content':'system'},{'role':'user','content':'Проверь canonical_test'},
            {'role':'assistant','tool_calls':[{'id':'canonical_call','type':'function','function':{'name':'run_project_command','arguments':'{}'}}]},
            {'role':'tool','tool_call_id':'canonical_call','content':raw}]
        original=deepcopy(messages);projected,_=smart_compact_messages(messages,4000,2,1)
        evidence=json.loads(projected[-1]['content'])
        self.assertEqual(evidence['source_tool_call_id'],'canonical_call');self.assertIn('canonical_test',evidence['output_excerpt'])
        self.assertEqual(messages,original)

    def test_archived_command_keeps_failure_summary_and_call_reference(self):
        messages=[{'role':'system','content':'system'},{'role':'user','content':'Проверь задачу'}]
        for index in range(6):messages.extend([
            {'role':'assistant','tool_calls':[{'id':f'check_{index}','type':'function','function':{'name':'run_project_command','arguments':'{}'}}]},
            {'role':'tool','tool_call_id':f'check_{index}','content':json.dumps({'ok':False,'exit_code':7,'output':'FAILED: test_failure_summary'})}])
        messages.append({'role':'user','content':'Что сломалось?'})
        projected,_=smart_compact_messages(messages,5000,2,len(messages)-1)
        archive=next(message['content'] for message in projected if message['role']=='assistant' and message.get('content','').startswith('[Архив'))
        self.assertIn('test_failure_summary',archive);self.assertIn('"exit_code": 7',archive);self.assertIn('"source_tool_call_id": "check_',archive)

    def test_archive_never_becomes_system_permissions(self):
        messages=[{'role':'system','content':'Original system'},{'role':'user','content':'Не меняй дизайн'}]
        messages.extend({'role':'assistant','content':'x'*500} for _ in range(30));messages.append({'role':'user','content':'Задача'})
        result,_=smart_compact_messages(messages,1800,2,len(messages)-1)
        self.assertEqual(result[0]['content'],'Original system');self.assertEqual(sum(m['role']=='system' for m in result),1)
        self.assertTrue(any(m['role']=='assistant' and 'compressed_history' in m.get('content','') for m in result))

    def test_repeated_tool_facts_are_deduplicated_and_history_unchanged(self):
        messages=[{'role':'system','content':'system'},{'role':'user','content':'Проверь'}]
        for index in range(15):messages.extend([{'role':'assistant','tool_calls':[{'id':str(index),'type':'function','function':{'name':'read_file','arguments':'{"path":"a.py"}'}}]},
            {'role':'tool','tool_call_id':str(index),'content':json.dumps({'ok':True,'path':'a.py','content':'x'*800})}])
        result,stats=smart_compact_messages(messages,4000,2,1)
        archive=next(m['content'] for m in result if m['role']=='assistant' and m.get('content','').startswith('[Архив'))
        self.assertEqual(archive.count('"path": "a.py"'),1);self.assertGreater(stats['archived_units'],0)


if __name__=='__main__':unittest.main()
