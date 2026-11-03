import fs from 'node:fs/promises';
import path from 'node:path';

// Use the build's configured name; never fall back to a stale product executable.
export async function resolvePackagedExecutable({ repoRoot, explicitPath }) {
  let executable;
  if (explicitPath) executable = path.resolve(explicitPath);
  else {
    const config = JSON.parse(await fs.readFile(path.join(repoRoot, 'electron-builder.json'), 'utf8'));
    const name = config.win?.executableName || config.executableName || config.productName;
    if (!name || path.basename(name) !== name) throw new Error('Invalid packaged executable name');
    executable = path.resolve(repoRoot, config.directories?.output || 'dist', 'win-unpacked', `${name}.exe`);
  }
  if (!(await fs.stat(executable)).isFile()) throw new Error(`Packaged executable is not a file: ${executable}`);
  return executable;
}
