"""Cancellable desktop worker using the same search as agent tools."""
import threading
from agent.security import canonical_root
from agent.operation_context import OperationContext
from agent.workspace_search import search_project, EXCLUDED


class ProjectSearchService:
    def __init__(self):
        self.thread = None
        self.cancelled = OperationContext(5)
        self.lock = threading.RLock()
        self.running = False

    def start(self, root, params, respond):
        with self.lock:
            if self.running:
                raise ValueError('Предыдущий поиск ещё завершается')
            snapshot_root = canonical_root(root)
            snapshot_params = dict(params)
            if snapshot_params.get('mode') in ('symbols','outline'):
                from agent.project_index import get_index
                get_index(snapshot_root,create=True)
            self.running = True
            self.cancelled = cancelled = OperationContext(5)

            def run_search():
                try:
                    response = search_project(snapshot_root, snapshot_params, cancelled)
                except Exception as exc:
                    response = {'ok':False, 'error':str(exc)[:500]}
                with self.lock:
                    self.running = False
                respond(response)

            self.thread = threading.Thread(target=run_search, daemon=True, name='project-search')
            self.thread.start()

    def cancel(self):
        self.cancelled.set()
        return {'ok':True}

    def shutdown(self):
        self.cancel()
        if self.thread:
            self.thread.join(timeout=1)
