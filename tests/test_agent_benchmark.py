"""Validate benchmark ownership and held-out checks without a real model."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools import benchmark_agent as benchmark


class AgentBenchmarkTests(unittest.TestCase):
    def test_auto_budget_trial_is_explicit_and_manual_default_is_preserved(self):
        """The optional auto experiment reaches the existing engine without changing the manual baseline."""
        from agent import engine as module
        for mode in (None,'auto'):
            conversation=module.EventHook()
            stub=SimpleNamespace(failed=module.EventHook(),conversation_updated=conversation,write_approval_requested=module.EventHook(),
                _messages=[{'role':'system','content':'fixture'},{'role':'user','content':'fixture'},{'role':'assistant','content':'done'}],
                run=lambda:None,task_snapshot=lambda:{'status':'completed','tool_calls':0})
            connection={'base_url':'http://unused.invalid/v1','model':'fixture','tool_protocol':'json'}
            if mode:connection['budget_mode']=mode
            with patch.object(module,'AgentEngine',return_value=stub) as factory,patch.object(benchmark,'resource_sample',return_value=None):
                result=benchmark.run_case(self.root,'bugfix',connection,Path(self.directory.name)/'profile')
            self.assertEqual(factory.call_args.kwargs['settings']['budget_mode'],mode or 'manual')
            self.assertEqual(result['generation_settings']['context_window'],8192)

    def setUp(self):
        self.directory=tempfile.TemporaryDirectory();self.addCleanup(self.directory.cleanup)
        self.root=Path(self.directory.name)/'project';benchmark.build_project(self.root,'small')

    def test_fixture_is_deterministic_and_reset_touches_only_owned_sources(self):
        """Reset cannot erase unrelated files or silently adopt another directory."""
        extra=self.root/'manual.txt';extra.write_text('keep')
        target=self.root/'app/totals.py';target.write_text('changed')
        benchmark.reset_project(self.root)
        self.assertEqual(extra.read_text(),'keep');self.assertEqual(target.read_text(),benchmark.FILES['app/totals.py'])
        (self.root/'.neutral-benchmark.json').write_text('{}')
        with self.assertRaises(ValueError):benchmark.reset_project(self.root)

    def test_initial_bug_fails_and_real_minimal_fix_passes(self):
        """The oracle checks behavior rather than trusting an agent's final answer."""
        self.assertFalse(benchmark.fixture_validation(self.root,'bugfix')['passed'])
        target=self.root/'app/totals.py';target.write_text(target.read_text().replace('1.1','1.2'))
        self.assertTrue(benchmark.fixture_validation(self.root,'bugfix')['passed'])

    def test_multifile_requires_definition_and_caller(self):
        """Renaming only the declaration cannot count as a successful multi-file edit."""
        target=self.root/'app/totals.py';target.write_text(target.read_text().replace('tax_total','grand_total'))
        self.assertFalse(benchmark.fixture_validation(self.root,'multifile')['passed'])
        caller=self.root/'app/invoice.py';caller.write_text(caller.read_text().replace('tax_total','grand_total'))
        self.assertTrue(benchmark.fixture_validation(self.root,'multifile')['passed'])
        caller.write_text(caller.read_text()+'\nraise RuntimeError("not executed")\n')
        self.assertFalse(benchmark.fixture_validation(self.root,'multifile')['passed'])

    def test_model_code_is_not_imported_or_executed_by_oracle(self):
        """Arbitrary calls, module effects and changed signatures are rejected without execution."""
        samples=['raise RuntimeError("not executed")\n',
            'def tax_total(subtotal):\n    return __import__("os").system("not executed")\n',
            'def tax_total(subtotal, *, required):\n    return subtotal * 1.2\n',
            'def tax_total(subtotal=__import__("os")):\n    return subtotal * 1.2\n']
        for text in samples:
            with self.subTest(text=text):
                (self.root/'app/totals.py').write_text(text)
                self.assertFalse(benchmark.fixture_validation(self.root,'bugfix')['passed'])

    def test_search_reports_coverage_and_real_paths(self):
        """Existing search sees fixture sources while protected paths never become hits."""
        from agent import task_store
        with patch.object(task_store,'TASK_DIR',Path(self.directory.name)/'profile/tasks'):
            result=benchmark.search_measurement(self.root,2)
        self.assertEqual(result['recall_at_10'],1);self.assertEqual(result['samples'],2)
        self.assertEqual(set(result['returned_paths']),{'app/totals.py','app/invoice.py'})

    def test_report_serialization_is_strict_and_atomic(self):
        """A report is valid UTF-8 JSON and cannot silently accept non-finite metrics."""
        destination=Path(self.directory.name)/'report.json';benchmark.save_report(destination,{'text':'Проверка','passed':False})
        self.assertEqual(json.loads(destination.read_text(encoding='utf-8'))['text'],'Проверка')
        with self.assertRaises(ValueError):benchmark.save_report(destination,{'bad':float('nan')})
        self.assertEqual(json.loads(destination.read_text(encoding='utf-8'))['passed'],False)

    def test_censored_experiment_is_distinct_from_incorrect_code(self):
        """A correct diff at the fixed trial cutoff must not be described as an incorrect edit."""
        case={'validation':{'passed':True},'diff_correct':True,'failures':[],'passed':False,'status':'paused',
            'stop_reason':'Остановлено: достигнут лимит циклов модели (10).'}
        outcome=benchmark.case_outcome(case)
        self.assertTrue(outcome['task_correct']);self.assertTrue(outcome['experiment_limit_reached'])
        self.assertFalse(outcome['completion_observed']);self.assertFalse(outcome['end_to_end_passed'])
        case['validation']['passed']=False;self.assertFalse(benchmark.case_outcome(case)['task_correct'])

    def test_location_oracle_does_not_accept_numeric_or_path_prefixes(self):
        """Line 10 or another directory cannot masquerade as app/totals.py:1."""
        for answer in ('app/totals.py:10','other/app/totals.py:1','myapp/totals.py:1'):
            self.assertFalse(benchmark.source_location_matches(answer,'app/totals.py:1'))
        self.assertTrue(benchmark.source_location_matches('`app/totals.py:1` — definition','app/totals.py:1'))

    def test_correct_location_without_successful_tool_evidence_is_not_success(self):
        """A guessed path or a failed read cannot count as verified code discovery."""
        from agent import engine as module
        for receipt in (None,{'ok':False,'path':'app/totals.py'}):
            messages=[{'role':'user','content':'fixture'}]
            if receipt:messages.append({'role':'tool','tool_call_id':'failed','content':json.dumps(receipt)})
            messages.append({'role':'assistant','content':'app/totals.py:1'})
            conversation=module.EventHook()
            stub=SimpleNamespace(failed=module.EventHook(),conversation_updated=conversation,write_approval_requested=module.EventHook(),
                _messages=[{'role':'system','content':'fixture'},*messages],
                run=lambda:conversation.emit(messages),task_snapshot=lambda:{'status':'completed','tool_calls':0})
            with patch.object(module,'AgentEngine',return_value=stub),patch.object(benchmark,'resource_sample',return_value=None):
                result=benchmark.run_case(self.root,'definition',{'base_url':'http://unused.invalid/v1','model':'fixture','tool_protocol':'json'},Path(self.directory.name)/'profile')
            self.assertFalse(result['passed']);self.assertEqual(result['inspected_paths'],[])


if __name__=='__main__':unittest.main()
