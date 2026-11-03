"""Read-only product audit probes: synthetic model replies, temporary task files.

Run from the repository root with .venv-test/Scripts/python.exe.
This is an audit of observed behavior, not a passing regression specification.
No model server, user profile, installed application or project data is modified.
"""
from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
import threading
import uuid
from types import SimpleNamespace as NS
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent import engine as engine_module, task_store, companion_preferences
from agent.context_manager import ContextManager
from agent.json_tools import prepare_json_request
from agent.smart_context import compact_tool_result
from agent.task_activity import recover_tools
from agent.tools import TOOL_DEFINITIONS, read_file, search_text
from agent.verifier import StageVerifier
from core.python.extension_service import ExtensionService
from core.python.task_service import TaskService


def chunk(text=None, calls=None, finish='stop'):
    return NS(choices=[NS(delta=NS(content=text, tool_calls=calls or []), finish_reason=finish)])


def tool(name, args, identity='call_a', index=0):
    return NS(index=index, id=identity, function=NS(name=name, arguments=json.dumps(args)))


class Stream:
    def __init__(self, chunks):
        self.chunks = chunks

    def __iter__(self):
        return iter(self.chunks)

    def close(self):
        pass


def engine_probe(root, replies, prompt='Проверь результат', **options):
    class Client:
        def __init__(self, *args, **kwargs):
            self.replies = iter(replies)

        def create(self, **kwargs):
            if not kwargs.get('stream'):
                return NS(choices=[NS(message=NS(content='{"complete":true}'))])
            return Stream(next(self.replies))

        def close(self):
            pass

    errors, results = [], []
    with ExitStack() as stack:
        stack.enter_context(patch.object(task_store, 'TASK_DIR', root / 'tasks'))
        stack.enter_context(patch.object(engine_module, 'ModelClient', Client))
        verifier = stack.enter_context(patch.object(StageVerifier, 'verify', return_value={'ok': False}))
        engine = engine_module.AgentEngine('http://unused.invalid', '', 'audit', str(root),
            prompt, auto_memory=False, task_id=uuid.uuid4().hex,
            settings={'max_agent_turns': 3}, **options)
        engine.failed.connect(errors.append)
        engine.finished_text.connect(results.append)
        engine.run()
        state = engine.task_snapshot()
        return {'status': state['status'], 'errors': errors, 'results': results,
                'test_results': state['test_results'], 'verifier_calls': verifier.call_count}


def main():
    observations = {}
    with tempfile.TemporaryDirectory(prefix='neutral-core-audit-') as directory:
        root = Path(directory)
        observations['truncated_answer'] = engine_probe(root,
            [[chunk('Ответ оборван на середине предложения', finish='length')]], allow_tools=False)
        observations['failed_check_marked_complete'] = engine_probe(root,
            [[chunk(calls=[tool('run_project_command', {})])], [chunk('Готово, всё работает.')]],
            prompt='Исправь код и добейся успешного прохождения тестов.',
            tool_definitions=[{'type': 'function', 'function': {'name': 'run_project_command'}}],
            tool_handler=lambda *_: {'ok': False, 'exit_code': 7, 'output': '1 test failed'})
        observations['malformed_write_aborts_run'] = engine_probe(root,
            [[chunk(calls=[tool('write_file', {'path': None, 'content': 'x', 'overwrite': False})])],
             [chunk('Некорректный путь; исправьте аргументы.')]],
            tool_definitions=TOOL_DEFINITIONS)

        synthetic_outputs = {
            'command': {'ok': False, 'exit_code': 7, 'output': 'AUDIT_FAILURE_DETAIL ' * 600},
            'mcp': {'ok': True, 'content': [{'type': 'text', 'text': 'AUDIT_MCP_EVIDENCE ' * 600}]},
        }
        for label, value in synthetic_outputs.items():
            content, changed = compact_tool_result(json.dumps(value), '', 6000)
            observations['compaction_' + label] = {'changed': changed, 'result': json.loads(content)}

        messages = [{'role': 'system', 'content': 'system'}, {'role': 'user', 'content': 'Task'},
            {'role': 'assistant', 'tool_calls': [
                {'id': identity, 'type': 'function', 'function': {'name': 'external_action', 'arguments': '{}'}}
                for identity in ('done', 'pending')]},
            {'role': 'tool', 'tool_call_id': 'done', 'content': '{"ok":true,"receipt":"AUDIT_RECEIPT"}'}]
        projected = ContextManager().build(messages)
        state = {'tool_activity': [{'id': 1, 'call_id': 'pending', 'message_index': 2,
                                   'tool': 'external_action', 'status': 'running'}]}
        recover_tools(state, messages)
        observations['interrupted_batch'] = {
            'canonical_retains_receipt': 'AUDIT_RECEIPT' in json.dumps(messages),
            'projection_retains_receipt': 'AUDIT_RECEIPT' in json.dumps(projected),
            'recovered_external_status': state['tool_activity'][0]['status']}

        short = ContextManager(12000).build(messages[:2])
        definitions = [{'type': 'function', 'function': {'name': f'mcp_example_{i}',
            'description': 'description', 'parameters': {'type': 'object', 'properties': {
                'value': {'type': 'string', 'description': 'schema ' * 3000}}}}} for i in range(8)]
        request, _, _ = prepare_json_request({'messages': short, 'tools': definitions})
        observations['schema_budget'] = {'configured_max_context_chars': 12000,
            'projected_message_chars': len(json.dumps(short)),
            'json_protocol_message_chars_after_adapter': len(json.dumps(request['messages']))}

        (root / '.gitignore').write_text('.env\n', encoding='utf8')
        (root / '.env').write_text('PASSWORD=AUDIT_SYNTHETIC_ONLY\n', encoding='utf8')
        observations['ignored_file_policy'] = {
            'read_dotenv_ok': read_file(root, '.env')['ok'],
            'search_includes_dotenv': any(m['path'] == '.env' for m in search_text(root, 'PASSWORD')['matches'])}

        extensions = ExtensionService(root / 'extensions')
        with patch.object(extensions.mcp, 'operation', return_value={'ok': True, 'tools': [
                {'name': 'echo', 'description': 'audit', 'parameters': {'type': 'object'}}]}):
            for identity in ('same_server_prefix_123456_one', 'same_server_prefix_123456_two'):
                extensions.configure({'kind': 'server_save', 'server': {
                    'id': identity, 'command': 'never-started', 'enabled': True}})
                extensions.discover_server(identity)
        snapshot = extensions.snapshot([])
        aliases = [t['function']['name'] for t in snapshot['definitions'] if t['function']['name'].startswith('mcp_')]
        observations['mcp_alias_collision'] = {'definitions': aliases, 'unique_routes': len(snapshot['external'])}

        service = TaskService.__new__(TaskService)
        service.lock = threading.RLock()
        service.task_running = False
        service.companion_config = {**companion_preferences.DEFAULT_PROFILE,
            'base_url': 'https://old.invalid/v1', 'stt_url': 'https://old.invalid/stt',
            'api_key': 'AUDIT_DUMMY_KEY', 'stt_api_key': 'AUDIT_DUMMY_STT_KEY'}
        with patch.object(companion_preferences, 'PROFILE_FILE', root / 'companion.json'):
            service.configure_companion({'base_url': 'https://new.invalid/v1', 'stt_url': 'https://new.invalid/stt'})
        observations['companion_credentials_after_endpoint_change'] = {
            'retains_model_key': bool(service.companion_config['api_key']),
            'retains_stt_key': bool(service.companion_config['stt_api_key'])}

    # Read the configured discovery deadline, not a historical constant or benchmark.
    import re
    main_source = (Path(__file__).resolve().parents[1] / 'apps/desktop/electron/main.ts').read_text(encoding='utf8')
    deadline = re.search(r"method === 'mcp_discover' \? (\d+)", main_source)
    observations['mcp_timeout_contract'] = {'electron_discovery_ms': int(deadline.group(1)) if deadline else 10000,
        'mcp_default_ms': 30000, 'mcp_max_ms': 120000}
    print(json.dumps(observations, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
