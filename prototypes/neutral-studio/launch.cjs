const path = require('node:path');
const { spawn } = require('node:child_process');
let electron;
try { electron = require('electron'); }
catch { console.error('Electron is required. Run npm install in the LocalAgent root first.'); process.exit(1); }
const env = { ...process.env };
delete env.ELECTRON_RUN_AS_NODE;
const child = spawn(electron, [path.join(__dirname, 'main.cjs'), ...process.argv.slice(2)], {
  cwd: __dirname, stdio: 'inherit', windowsHide: process.argv.includes('--capture') || process.argv.includes('--verify'), env,
});
child.on('error', error => { console.error(error.message); process.exitCode = 1; });
child.on('exit', code => { process.exitCode = code || 0; });
