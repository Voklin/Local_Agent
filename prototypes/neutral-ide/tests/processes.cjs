const {spawnSync}=require('node:child_process');
function sampleProcesses(rootPid){
 if(!Number.isInteger(rootPid)||rootPid<1)throw Error('Invalid PID');
 const script=`$rows=@(Get-CimInstance Win32_Process); $ids=[Collections.Generic.HashSet[int]]::new(); [void]$ids.Add(${rootPid}); do {$changed=$false; foreach($row in $rows){if($ids.Contains([int]$row.ParentProcessId) -and $ids.Add([int]$row.ProcessId)){$changed=$true}}} while($changed); @($ids | ForEach-Object {Get-Process -Id $_ -ErrorAction SilentlyContinue} | Select-Object Id,ProcessName,@{N='working_set_bytes';E={$_.WorkingSet64}},@{N='cpu_seconds';E={$_.TotalProcessorTime.TotalSeconds}}) | ConvertTo-Json -Compress`;
 const result=spawnSync('powershell.exe',['-NoLogo','-NoProfile','-NonInteractive','-Command',script],{encoding:'utf8',windowsHide:true,timeout:15000});
 if(result.status!==0)throw Error('Cannot sample owned process tree: '+result.stderr);const rows=JSON.parse(result.stdout);return Array.isArray(rows)?rows:[rows];
}
module.exports={sampleProcesses};
