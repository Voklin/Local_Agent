const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

function launch() {
  const handlers = {};
  const process = { env: { ELECTRON_RUN_AS_NODE: '1' }, argv: ['node', 'run.cjs', 'fixture.cjs'] };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'run.cjs'), 'utf8'), {
    require(id) {
      if (id === 'electron') return 'fixture-electron';
      if (id === 'node:child_process') return { spawn: () => ({ on: (event, callback) => { handlers[event] = callback; } }) };
      return require(id);
    },
    __dirname, process, console: { error() {} },
  });
  return { handlers, process };
}

test('normal exit zero succeeds', () => {
  const { handlers, process } = launch();
  handlers.exit(0, null);
  assert.equal(process.exitCode, 0);
});

test('nonzero exit code is preserved', () => {
  const { handlers, process } = launch();
  handlers.exit(7, null);
  assert.equal(process.exitCode, 7);
});

test('termination by signal fails', () => {
  const { handlers, process } = launch();
  handlers.exit(null, 'SIGTERM');
  assert.equal(process.exitCode, 1);
});

test('spawn error fails', () => {
  const { handlers, process } = launch();
  handlers.error(new Error('ENOENT'));
  assert.equal(process.exitCode, 1);
});

test('missing exit status fails', () => {
  const { handlers, process } = launch();
  handlers.exit(null, null);
  assert.equal(process.exitCode, 1);
});
