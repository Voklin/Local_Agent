import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { resolvePackagedExecutable } from './packaged-path.mjs';

async function fixture(t, names) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'leshy-package-path-'));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  await fs.writeFile(path.join(root, 'electron-builder.json'), JSON.stringify({ productName: 'LESHY', directories: { output: 'output' } }));
  await fs.mkdir(path.join(root, 'output/win-unpacked'), { recursive: true });
  for (const name of names) await fs.writeFile(path.join(root, 'output/win-unpacked', name), 'fixture');
  return root;
}

test('clean LESHY output resolves the current executable', async t => {
  const repoRoot = await fixture(t, ['LESHY.exe']);
  assert.equal(await resolvePackagedExecutable({ repoRoot }), path.join(repoRoot, 'output/win-unpacked/LESHY.exe'));
});

test('old Neutral output cannot replace a missing LESHY executable', async t => {
  const repoRoot = await fixture(t, ['Neutral.exe']);
  await assert.rejects(resolvePackagedExecutable({ repoRoot }), { code: 'ENOENT' });
});

test('LESHY is selected even when old Neutral output also exists', async t => {
  const repoRoot = await fixture(t, ['Neutral.exe', 'LESHY.exe']);
  assert.equal(await resolvePackagedExecutable({ repoRoot }), path.join(repoRoot, 'output/win-unpacked/LESHY.exe'));
});

test('an explicit fresh output path is used exactly', async t => {
  const repoRoot = await fixture(t, []);
  const explicitPath = path.join(repoRoot, 'fresh.exe');
  await fs.writeFile(explicitPath, 'fixture');
  assert.equal(await resolvePackagedExecutable({ repoRoot, explicitPath }), explicitPath);
});
