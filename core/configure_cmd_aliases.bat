@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title CONFIGURAR ALIAS ESTILO LINUX EN CMD (WINDOWS)

for %%I in ("%~dp0.") do set "CORE_DIR=%%~fI"
for %%I in ("%~dp0..") do set "SCRIPT_DIR=%%~fI"
for %%I in ("%~dp0..\..\epub-generator") do set "PROJECT_DIR=%%~fI"

echo ====================================================================
echo      CONFIGURACION DE ALIAS ESTILO LINUX PARA CMD Y POWERSHELL
echo ====================================================================
echo.

call :FIND_PYTHON

if "!PY_CMD!"=="" (
    echo [!] No se detecto un interprete de Python funcional en este equipo.
    echo     [El comando 'python' apunta a la tienda Microsoft Store]
    echo.
    echo Para trabajar con el orquestador y los alias se requiere Python 3.10+.
    echo.
    set /p "INSTALL_PY=¿Deseas instalar Python 3.11 y dependencias ahora mismo? [S/n]: "
    if "!INSTALL_PY!"=="" set "INSTALL_PY=S"
    if /i "!INSTALL_PY!"=="S" (
        call "%SCRIPT_DIR%\installers\install_epub_deps.bat"
        call :FIND_PYTHON
    )
)

if not "!PY_CMD!"=="" (
    "!PY_CMD!" "%CORE_DIR%\alias_manager.py" apply
    if !ERRORLEVEL! EQU 0 (
        echo.
        "!PY_CMD!" "%CORE_DIR%\alias_manager.py" list
        if /i not "%~1"=="--nopause" pause
        exit /b 0
    )
)

:: Fallback si el usuario no tiene Python todavia
echo.
echo [INFO] Agregando la carpeta bin al PATH del usuario...
set "BIN_DIR=%SCRIPT_DIR%\bin"
powershell -NoProfile -Command "$b = '%BIN_DIR%'; $u = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($u -notlike '*' + $b + '*') { [Environment]::SetEnvironmentVariable('Path', ($u.TrimEnd(';') + ';' + $b), 'User') }" >nul 2>nul

echo [OK] Comandos globales listos en %BIN_DIR%.
echo [AVISO] Ejecuta la opcion [1] en setup_all.bat para instalar Python y librerias.

if /i not "%~1"=="--nopause" pause
exit /b 0

:: ====================================================================
:: SUBRUTINA: BUSCADOR DE PYTHON ROBUSTO
:: ====================================================================
:FIND_PYTHON
set "PY_CMD="

:: 1. Entorno virtual de epub-generator
if exist "%PROJECT_DIR%\.venv\Scripts\python.exe" (
    set "PY_CMD=%PROJECT_DIR%\.venv\Scripts\python.exe"
    exit /b 0
)

:: 2. Python en AppData del usuario (3.11, 3.12, 3.10)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    exit /b 0
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    exit /b 0
)
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    exit /b 0
)

:: 3. Archivos de Programa
if exist "%ProgramFiles%\Python311\python.exe" (
    set "PY_CMD=%ProgramFiles%\Python311\python.exe"
    exit /b 0
)

:: 4. py launcher oficial
py -3 -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=py -3"
    exit /b 0
)

:: 5. Python en PATH del sistema (comprobando que ejecute codigo real, no el stub de MS Store)
python -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
    exit /b 0
)

set "PY_CMD="
exit /b 1
