param(
    [string]$PythonPath='',
    [string]$ModelPath=(Join-Path $env:LOCALAPPDATA 'LocalCodingAgent/speech/piper/ru_RU-irina-medium.onnx')
)
$ErrorActionPreference='Stop'
$piperDirectory=Join-Path $env:LOCALAPPDATA 'LocalCodingAgent/piper-runtime'
$piperPython=Join-Path $piperDirectory 'Scripts/python.exe'
if(-not(Test-Path -LiteralPath $piperPython)) {
    if($PythonPath) { & $PythonPath -m venv $piperDirectory }
    else { & py -3.12 -m venv $piperDirectory }
    if($LASTEXITCODE -ne 0) { throw 'Python 3.12 is required to create the Piper environment.' }
}
if(-not(Test-Path -LiteralPath $ModelPath) -or -not(Test-Path -LiteralPath ($ModelPath+'.json'))) {
    throw 'Download the Piper ONNX voice and matching .onnx.json first; see README.md.'
}
$ErrorActionPreference='Continue'
& $piperPython -c "import piper"
if($LASTEXITCODE -ne 0) {
    & $piperPython -m pip install 'piper-tts==1.8.0'
    if($LASTEXITCODE -ne 0) { throw 'Could not install Piper.' }
}
$ErrorActionPreference='Stop'
& $piperPython (Join-Path $PSScriptRoot 'piper_server.py') --model $ModelPath
exit $LASTEXITCODE
