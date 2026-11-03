process.env.LESHY_ACCEPTANCE_TEST='1';
if(process.argv.includes('--json'))process.env.LESHY_ACCEPTANCE_JSON='1';
process.argv[2]='neutral-ide-integration.cjs';
require('./run.cjs');
