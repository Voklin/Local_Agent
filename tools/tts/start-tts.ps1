param([ValidateSet('cpu','cuda','auto')][string]$Device='cpu')
$ErrorActionPreference='Stop'
$ttsDirectory=Join-Path $env:LOCALAPPDATA 'LocalCodingAgent/tts-runtime'
$ttsPython=Join-Path $ttsDirectory 'Scripts/python.exe'
if (-not (Test-Path -LiteralPath $ttsPython)) {
    Write-Host 'Creating isolated TTS environment. Requires Python 3.12 (py launcher).'
    & py -3.12 -m venv $ttsDirectory
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12 with the py launcher, then retry.' }
    & $ttsPython -m pip install torch --index-url https://download.pytorch.org/whl/cpu
    if ($LASTEXITCODE -ne 0) { throw 'Could not install CPU PyTorch' }
}
& $ttsPython -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Could not install TTS requirements; retry when network is available.' }
& $ttsPython (Join-Path $PSScriptRoot 'qwen_server.py') --device $Device
exit $LASTEXITCODE
