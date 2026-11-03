"""Deterministic stage verification. It does not modify files or grant permissions."""
from __future__ import annotations
from copy import deepcopy
from .task_contract import command_key, acceptance_summary
from .verification_evidence import configured_check,capture_witness,assess_evidence

class StageVerifier:
    def record_command(self, task, arguments, result):
        """Keep the latest outcome per exact command; unrelated success cannot erase failure."""
        key = command_key(arguments)
        configured=configured_check(task,arguments)
        if configured:key+='_'+configured['id']
        checks = task.setdefault('test_results', [])
        entry = {'id': key, 'kind': 'command', 'program': str(arguments.get('program', ''))[:300],
                 'arguments':arguments.get('arguments',[]),'cwd':arguments.get('cwd','.'),
                 'purpose':configured['purpose'] if configured else str(arguments.get('purpose','Назначение не задано'))[:300],
                 'check_id':configured['id'] if configured else '',
                 'generation':result.get('workspace_generation',0),
                 'workspace_revision':result.get('workspace_revision'),
                 'command':deepcopy(arguments),'verification_receipt':deepcopy(result.get('verification_receipt')),
                 'code':result.get('code'),
                 'exit_code': result.get('exit_code'), 'ok': result.get('ok') is True and type(result.get('exit_code')) is int and result.get('exit_code') == 0}
        checks[:] = [item for item in checks if item.get('id') != key] + [entry]
        task['verification_schema']=2

    def record_diagnostics(self, task, args, result):
        """Record an LSP receipt separately from process exit codes; failure cannot erase another check."""
        check=next((c for c in task['options']['checks'] if c['id']==args.get('check_id')),None)
        if not check:return
        entry={'id':'diagnostics_'+check['id'],'kind':'diagnostics','program':'LSP','arguments':check['arguments'],'purpose':check['purpose'],'check_id':check['id'],
            'ok':result.get('ok') is True,'exit_code':None,'code':result.get('code'),'verification_receipt':deepcopy(result.get('verification_receipt')),'diagnostics':result.get('diagnostics',[])}
        checks=task.setdefault('test_results',[]);checks[:]=[r for r in checks if r['id']!=entry['id']]+[entry]

    def command_summary(self, task):
        """Report command evidence only; exit zero is not proof of every user criterion."""
        checks = [item for item in task.get('test_results', []) if item.get('kind') in ('command','diagnostics')]
        from .verification_plan import required_checks
        required=required_checks(task)
        if not checks and not required and task.get('options',{}).get('checks'):return {'status':'not_run','execution_status':'not_run','summary':'Заданные проверки не относятся к затронутым файлам по шаблонам пользователя.'}
        if not checks:return {'status': 'incomplete' if required and not task.get('options',{}).get('read_only') else 'not_run',
            'execution_status':'not_run', 'summary': 'Проверка не подтверждена: команды проверки не запускались.'}
        receipts=[item.get('verification_receipt') for item in checks]
        workspace=any(isinstance(r,dict) and isinstance(r.get('scope'),dict) and r['scope'].get('kind')=='workspace' for r in receipts)
        task['workspace_revision']=capture_witness(task.get('project_root',''),{'kind':'workspace'}) if workspace else None
        for item in checks:
            evidence=assess_evidence(task,item,task['workspace_revision'])
            item.update(evidence_status=evidence['status'],evidence_summary=evidence['summary'],coverage=evidence['coverage'])
        current=[item for item in checks if item['evidence_status']=='current']
        facts={'execution_status':'passed' if all(c.get('ok') for c in checks) else 'failed',
            'project_complete':len(current)==len(checks) and all(c['coverage']['project_complete'] for c in current)}
        if any(not item.get('ok') for item in checks):return {**facts,'status': 'failed', 'summary': 'Есть команды с ошибкой или неподтверждённым результатом. Повторите их на текущих исходниках.'}
        if len(current)!=len(checks):return {**facts,'status':'stale','summary':next(c['evidence_summary'] for c in checks if c['evidence_status']!='current')}
        from .verification_plan import required_checks
        configured=required_checks(task)
        if any(not any(c.get('check_id')==check['id'] for c in current) for check in configured):
            return {**facts,'status':'incomplete','summary':'Не все заданные проверки выполнены.'}
        if not facts['project_complete']:
            return {**facts,'status':'scoped_passed','summary':'Проверки прошли на снимке выбранных файлов и объявленных зависимостей. Актуальность всего проекта не подтверждена.'}
        return {**facts,'status': 'commands_passed', 'summary': 'Команды завершились успешно на актуальном снимке проекта. Это не подтверждает все требования задачи автоматически.'}

    def refresh(self,task):
        """Refresh evidence after reload/rollback without changing run lifecycle."""
        from .task_graph import refresh_steps
        refresh_steps(task)
        task['verification']=self.command_summary(task)
        task['acceptance_evidence']=acceptance_summary(task)
        uncovered=[c['description'] for c in task['acceptance_evidence'] if c['status'] not in ('checks_passed','scoped_checks_passed')]
        task['verification']['uncovered']=uncovered
        if uncovered and task['verification']['status'] in ('commands_passed','scoped_passed'):
            task['verification'].update(status='incomplete',summary='Команды прошли; часть критериев ещё не подтверждена.')
        return task['verification']

    def verify(self, stage_id, *, tool_events=None, final_text="", stop_reason="", task=None):
        if task is not None:
            self.refresh(task)
            if task.get('recovery_items') or task.get('recovery_error') or task.get('snapshot_attention'):
                return {'ok':False,'reason':'Исход действия неизвестен. Проверьте карточку восстановления перед продолжением.'}
            if task['verification']['status']=='failed':
                return {'ok':False,'reason':'Проверка не прошла: есть команды с ошибкой или неподтверждённым результатом. Проверьте журнал и продолжите задачу.'}
            if task['verification']['status'] in ('stale','incomplete'):
                return {'ok':False,'reason':task['verification']['summary']}
            pending=[n for n in task.get('plan_steps',[]) if not n.get('advisory') and n.get('status')!='done']
            if pending:return {'ok':False,'reason':'План не подтверждён: '+', '.join(n['title'] for n in pending)[:350]+'. Проверьте evidence и продолжите задачу.'}
            if stop_reason:return {'ok':False,'reason':stop_reason}
            return {'ok':bool(final_text.strip()),'reason':'Ответ получен; свидетельства команд учтены.' if final_text.strip() else 'Модель не сформировала текстовый ответ.'}
        events=tool_events or []
        if stop_reason: return {"ok":False,"reason":stop_reason}
        if stage_id in ("implementation", "verification"):
            if any(e.get("tool")=="write_file" and e.get("ok") for e in events):
                return {"ok":True,"reason":"Есть подтверждённый результат инструмента."}
        if final_text.strip(): return {"ok":True,"reason":"Модель сформировала итоговый ответ."}
        return {"ok":False,"reason":"Нет проверяемого результата."}
