@echo off
setlocal
set "BIN_DIR=%~dp0"
set "ROOT_DIR=%BIN_DIR%.."
set "PROJECT_DIR=%ROOT_DIR%\..\epub-generator"
cd /d "%PROJECT_DIR%"
where.exe antigravity-ide >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    call antigravity-ide . 2>nul
) else (
    explorer .
)
