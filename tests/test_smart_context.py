from copy import deepcopy
import json
import unittest
from agent.smart_context import smart_compact_messages,compact_tool_result


class SmartContextTests(unittest.TestCase):
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
