"""Run isolated deterministic readiness workflows and save per-test evidence as JSON."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    'tests.migration.test_agent_readiness',
    'tests.migration.test_child_execution',
    'tests.migration.test_run_owner_restart',
    'tests.migration.test_task_graph_execution',
    'tests.test_context_builder',
    'tests.test_project_index',
    'tests.test_services_and_sessions',
    'tests.test_project_command',
]


class EvidenceResult(unittest.TextTestResult):
    """Keep test outcomes and timings alongside unittest's traceback log."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def startTest(self, test):
        self.started = time.perf_counter()
        self.record = {'test': test.id(), 'expected': test.shortDescription() or test.id().split('.')[-1],
            'status': 'PASSED'}
        super().startTest(test)

    def addFailure(self, test, err):
        self.record.update(status='FAILED', error=self._exc_info_to_string(err, test))
        super().addFailure(test, err)

    def addError(self, test, err):
        self.record.update(status='FAILED', error=self._exc_info_to_string(err, test))
        super().addError(test, err)

    def addSkip(self, test, reason):
        self.record.update(status='UNVERIFIED', reason=reason)
        super().addSkip(test, reason)

    def addSubTest(self, test, subtest, err):
        if err:self.record.update(status='FAILED', error=self._exc_info_to_string(err, test))
        super().addSubTest(test, subtest, err)

    def stopTest(self, test):
        self.record['seconds'] = round(time.perf_counter()-self.started, 3)
        self.records.append(self.record)
        super().stopTest(test)


def main():
    """Use a fresh profile and writable temp root; never inherit the user's Neutral data."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'artifacts/readiness/scenarios.json')
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT/'tests/migration'))
    temp_root = ROOT/'.test-tmp'
    temp_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='readiness-', dir=temp_root) as directory:
        os.environ.update(TEMP=directory, TMP=directory, LOCALAPPDATA=str(Path(directory)/'profile'))
        tempfile.tempdir = directory
        suite = unittest.defaultTestLoader.loadTestsFromNames(SUITES)
        result = unittest.TextTestRunner(verbosity=2, resultclass=EvidenceResult).run(suite)
        report = {'created_utc': datetime.now(timezone.utc).isoformat(),
            'provider': 'deterministic localhost fixtures', 'real_model_quality': 'UNVERIFIED by this suite',
            'python': sys.version, 'tests': result.testsRun, 'passed': result.wasSuccessful(),
            'skipped': len(result.skipped), 'records': result.records}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
