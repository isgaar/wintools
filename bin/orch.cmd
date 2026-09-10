@echo off
setlocal
set "BIN_DIR=%~dp0"
set "ROOT_DIR=%BIN_DIR%.."
set "PROJECT_DIR=%ROOT_DIR%\..\epub-generator"
cd /d "%PROJECT_DIR%"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m amazon_publisher.translator.orchestrator %*
) else (
    python -m amazon_publisher.translator.orchestrator %*
)
