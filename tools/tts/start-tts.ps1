param(
    [ValidateSet('cpu','cuda','auto')][string]$Device='cpu',
    [string]$PythonPath='',
    [ValidateSet('voicedesign-1.7b','custom-0.6b')][string]$Model='voicedesign-1.7b',
    [ValidateSet('Ono_Anna','Serena','Vivian','Sohee','Ryan','Aiden','Uncle_Fu','Dylan','Eric')][string]$Speaker='Ono_Anna',
    [switch]$LowMemory,
    [switch]$InstallOnly
)
$ErrorActionPreference='Stop'
$ttsDirectory=Join-Path $env:LOCALAPPDATA 'LocalCodingAgent/tts-runtime'
$ttsPython=Join-Path $ttsDirectory 'Scripts/python.exe'
if (-not (Test-Path -LiteralPath $ttsPython)) {
    Write-Host 'Creating isolated TTS environment. Requires Python 3.12.'
    if ($PythonPath) {
        & $PythonPath -c "import sys; assert sys.version_info[:2] == (3,12), 'Python 3.12 required'"
        if ($LASTEXITCODE -ne 0) { throw 'PythonPath must point to Python 3.12.' }
        & $PythonPath -m venv $ttsDirectory
    } else {
        & py -3.12 -m venv $ttsDirectory
    }
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12 with the py launcher, then retry.' }
}
# Retry incomplete installations too; preserve an already installed CUDA build.
# Windows PowerShell 5 treats native stderr (including pip notices) as errors.
# Native failures below are checked using their exit codes instead.
$ErrorActionPreference='Continue'
$ttsProbe='import torch,torchaudio'
if ($Device -eq 'cuda') { $ttsProbe+=';assert torch.cuda.is_available()' }
& $ttsPython -c "import subprocess,sys;sys.exit(subprocess.run([sys.executable,'-c',sys.argv[1]],capture_output=True).returncode)" $ttsProbe
if ($LASTEXITCODE -ne 0) {
    $ttsIndex='https://download.pytorch.org/whl/cpu'
    $ttsVersion='2.11.0+cpu'
    if ($Device -eq 'cuda') { $ttsIndex='https://download.pytorch.org/whl/cu128'; $ttsVersion='2.11.0+cu128' }
    & $ttsPython -m pip install "torch==$ttsVersion" "torchaudio==$ttsVersion" --index-url $ttsIndex
    if ($LASTEXITCODE -ne 0) { throw 'Could not install matching PyTorch/torchaudio. Check network and NVIDIA driver for CUDA.' }
}
& $ttsPython -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Could not install TTS requirements; retry when network is available.' }
$ErrorActionPreference='Stop'
if ($InstallOnly) { Write-Host 'TTS dependencies installed. Model weights download on server startup.'; exit 0 }
$ttsArguments=@('--device',$Device,'--model',$Model,'--speaker',$Speaker)
if ($LowMemory) { $ttsArguments+=@('--dtype','bfloat16') }
& $ttsPython (Join-Path $PSScriptRoot 'qwen_server.py') @ttsArguments
exit $LASTEXITCODE
