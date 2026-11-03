@echo off
setlocal
cd /d "%~dp0"
if not defined LCA_PYTHON (
  if exist ".venv\Scripts\python.exe" set "LCA_PYTHON=%~dp0.venv\Scripts\python.exe"
)
call npm run dev
if errorlevel 1 pause
