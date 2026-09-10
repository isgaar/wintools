@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title CONFIGURAR ALIAS ESTILO LINUX EN CMD (WINDOWS)

set "CORE_DIR=%~dp0"
if "%CORE_DIR:~-1%"=="\" set "CORE_DIR=%CORE_DIR:~0,-1%"
set "SCRIPT_DIR=%CORE_DIR%\.."
set "PROJECT_DIR=%SCRIPT_DIR%\..\epub-generator"

echo ====================================================================
echo      CONFIGURACION DE ALIAS ESTILO LINUX PARA CMD Y POWERSHELL
echo ====================================================================
echo.

set "PY_CMD=python"
if exist "%PROJECT_DIR%\.venv\Scripts\python.exe" (
    set "PY_CMD=%PROJECT_DIR%\.venv\Scripts\python.exe"
)

"%PY_CMD%" "%CORE_DIR%\alias_manager.py" apply
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al aplicar los alias con alias_manager.py.
    if /i not "%~1"=="--nopause" pause
    exit /b 1
)

echo.
"%PY_CMD%" "%CORE_DIR%\alias_manager.py" list

if /i not "%~1"=="--nopause" pause
exit /b 0
