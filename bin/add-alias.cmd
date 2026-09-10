@echo off
setlocal
set "SCRIPT_DIR=%~dp0.."
set "PY_CMD=python"
if exist "%SCRIPT_DIR%\..\epub-generator\.venv\Scripts\python.exe" (
    set "PY_CMD=%SCRIPT_DIR%\..\epub-generator\.venv\Scripts\python.exe"
)
"%PY_CMD%" "%SCRIPT_DIR%\core\alias_manager.py" add %*
