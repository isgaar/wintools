@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title AGENT BRIDGE - epub-generator ^& Windows Scripts

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "VENV_PY=%SCRIPT_DIR%\..\epub-generator\.venv\Scripts\python.exe"
set "HUB_PY=%SCRIPT_DIR%\core\agent_hub.py"

:: Detectar intérprete de Python (preferir .venv de epub-generator)
if exist "%VENV_PY%" (
    set "PY_CMD=%VENV_PY%"
) else (
    where python >nul 2>nul
    if !ERRORLEVEL! EQU 0 (
        set "PY_CMD=python"
    ) else (
        echo [ERROR] No se encontro Python ni en .venv ni en el PATH del sistema.
        echo Ejecuta setup_all.bat primero para instalar dependencias.
        pause
        exit /b 1
    )
)

"%PY_CMD%" "%HUB_PY%" %*
exit /b %ERRORLEVEL%
