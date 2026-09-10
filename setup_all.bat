@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title WINDOWS SCRIPTS - Instalador y Gestor de Herramientas

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_DIR=%SCRIPT_DIR%\..\epub-generator"

call :FIND_PYTHON

if /i "%~1"=="--all" goto :OPT_ALL
if /i "%~1"=="--deps" goto :OPT_DEPS
if /i "%~1"=="--brave" goto :OPT_BRAVE
if /i "%~1"=="--gemini-cli" goto :OPT_GEMINI_CLI
if /i "%~1"=="--agy" goto :OPT_GEMINI_CLI
if /i "%~1"=="--git" goto :OPT_GIT
if /i "%~1"=="--aliases" goto :OPT_ALIASES
if /i "%~1"=="--alias" goto :OPT_ALIASES
if /i "%~1"=="--export-aliases" goto :OPT_EXPORT_ALIASES
if /i "%~1"=="--list-aliases" goto :OPT_LIST_ALIASES
if /i "%~1"=="--clean-locks" goto :OPT_CLEAN_LOCKS
if /i "%~1"=="--unlock" goto :OPT_CLEAN_LOCKS
if /i "%~1"=="--agent" goto :OPT_AGENT
if /i "%~1"=="--fix-ide" goto :OPT_FIX_IDE
if /i "%~1"=="--fix-antigravity" goto :OPT_FIX_IDE
if /i "%~1"=="--branch" goto :OPT_BRANCH
if /i "%~1"=="--branches" goto :OPT_BRANCHES
if /i "%~1"=="--sync-branches" goto :OPT_BRANCHES
if /i "%~1"=="--doc" goto :OPT_DOCS
if /i "%~1"=="--docs" goto :OPT_DOCS

:MENU
cls
echo ====================================================================
echo             GESTOR DE SCRIPTS DE WINDOWS (WINDOWS-SCRIPTS)
echo ====================================================================
echo.
echo  [1] Instalar dependencias de epub-generator (Python, .venv y librerias)
echo  [2] Instalar o verificar Brave Browser (Requerido para traducciones)
echo  [3] Instalar o verificar Gemini CLI (Antigravity CLI / agy)
echo  [4] Instalar o verificar Git para Windows
echo  [5] Configurar o importar todos los alias (orch, agyd, ag, epub...)
echo  [6] Realizar TODO (Git + Brave + Gemini CLI + Deps + Alias + Fix IDE) [Equipo nuevo]
echo  [7] Limpiar archivos de bloqueo huerfanos (.lock) del orquestador
echo  [8] Crear un nuevo alias y guardarlo en el repositorio
echo  [9] Exportar / Sincronizar alias locales hacia el repositorio
echo  [10] Iniciar Agent Bridge (Discord, auditoria paso a paso, guardia)
echo  [11] Corregir doble ventana e historiales en Antigravity IDE
echo  [12] Gestionar o cambiar ramas de libros en epub-generator (PT, WIP, Main...)
echo  [13] Ver documentacion del estado de ramas y libros trabajados (.md)
echo  [14] Salir
echo.
echo ====================================================================
set /p "CHOICE=Selecciona una opcion [1-14]: "

if "%CHOICE%"=="1" goto :OPT_DEPS
if "%CHOICE%"=="2" goto :OPT_BRAVE
if "%CHOICE%"=="3" goto :OPT_GEMINI_CLI
if "%CHOICE%"=="4" goto :OPT_GIT
if "%CHOICE%"=="5" goto :OPT_ALIASES
if "%CHOICE%"=="6" goto :OPT_ALL
if "%CHOICE%"=="7" goto :OPT_CLEAN_LOCKS
if "%CHOICE%"=="8" goto :OPT_ADD_CUSTOM
if "%CHOICE%"=="9" goto :OPT_EXPORT_ALIASES
if "%CHOICE%"=="10" goto :OPT_AGENT
if "%CHOICE%"=="11" goto :OPT_FIX_IDE
if "%CHOICE%"=="12" goto :OPT_BRANCHES
if "%CHOICE%"=="13" goto :OPT_DOCS
if "%CHOICE%"=="14" goto :END
echo.
echo [!] Opcion invalida.
timeout /t 2 >nul
goto :MENU

:OPT_ALL
call "%SCRIPT_DIR%\installers\install_git.bat" --nopause
call "%SCRIPT_DIR%\installers\install_brave.bat" --nopause
call "%SCRIPT_DIR%\installers\install_gemini_cli.bat" --nopause
call "%SCRIPT_DIR%\installers\install_epub_deps.bat"
call "%SCRIPT_DIR%\core\configure_cmd_aliases.bat" --nopause
call :SUB_FIX_IDE --nopause
goto :END

:OPT_DEPS
call "%SCRIPT_DIR%\installers\install_epub_deps.bat"
call :FIND_PYTHON
goto :END

:OPT_BRAVE
call "%SCRIPT_DIR%\installers\install_brave.bat"
if not "%~1"=="" goto :END
goto :MENU

:OPT_GEMINI_CLI
call "%SCRIPT_DIR%\installers\install_gemini_cli.bat"
if not "%~1"=="" goto :END
goto :MENU

:OPT_GIT
call "%SCRIPT_DIR%\installers\install_git.bat"
if not "%~1"=="" goto :END
goto :MENU

:OPT_ALIASES
if not "%~1"=="" (
    call "%SCRIPT_DIR%\core\configure_cmd_aliases.bat" --nopause
    call :FIND_PYTHON
    goto :END
)
call "%SCRIPT_DIR%\core\configure_cmd_aliases.bat"
call :FIND_PYTHON
goto :MENU

:OPT_EXPORT_ALIASES
call :FIND_PYTHON
if "%PY_CMD%"=="" (
    echo [!] Se requiere Python 3.10+ para exportar alias.
    echo     Ejecuta la opcion [1] para instalar Python y dependencias.
    if not "%~1"=="" goto :END
    pause
    goto :MENU
)
echo.
"%PY_CMD%" "%SCRIPT_DIR%\core\alias_manager.py" export
if not "%~1"=="" goto :END
pause
goto :MENU

:OPT_LIST_ALIASES
call :FIND_PYTHON
if "%PY_CMD%"=="" (
    echo [!] Se requiere Python 3.10+ para listar alias.
    echo     Ejecuta la opcion [1] para instalar Python y dependencias.
    if not "%~1"=="" goto :END
    pause
    goto :MENU
)
echo.
"%PY_CMD%" "%SCRIPT_DIR%\core\alias_manager.py" list
if not "%~1"=="" goto :END
pause
goto :MENU

:OPT_CLEAN_LOCKS
echo.
echo Limpiando archivos de bloqueo (.lock) en el orquestador...
set "STATE_DIR=%SCRIPT_DIR%\..\epub-generator\amazon_publisher\translator\orchestrator\state"
if exist "%STATE_DIR%" (
    del /f /q "%STATE_DIR%\*.lock" 2>nul
    echo [OK] Archivos .lock eliminados de %STATE_DIR%
) else (
    echo [!] Carpeta de estado no encontrada: %STATE_DIR%
)
if not "%~1"=="" goto :END
pause
goto :MENU

:OPT_AGENT
call "%SCRIPT_DIR%\agent.bat"
if not "%~1"=="" goto :END
goto :MENU

:OPT_ADD_CUSTOM
call :FIND_PYTHON
if "%PY_CMD%"=="" (
    echo [!] Se requiere Python 3.10+ para anadir alias.
    echo     Ejecuta la opcion [1] para instalar Python y dependencias.
    pause
    goto :MENU
)
cls
echo ====================================================================
echo      CREAR ALIAS PERSONALIZADO Y GUARDAR EN EL REPOSITORIO
echo ====================================================================
echo.
set /p "NEW_NAME=Escribe el nombre del comando/alias (ej: miweb, app): "
if "%NEW_NAME%"=="" (
    echo [!] El nombre no puede estar vacio.
    pause
    goto :MENU
)
set /p "NEW_PATH=Escribe la ruta de la carpeta (deja vacio para la carpeta actual): "
if "%NEW_PATH%"=="" set "NEW_PATH=%CD%"

echo.
"%PY_CMD%" "%SCRIPT_DIR%\core\alias_manager.py" add "%NEW_NAME%" "%NEW_PATH%"
echo.
pause
goto :MENU

:OPT_FIX_IDE
call :SUB_FIX_IDE
if not "%~1"=="" goto :END
pause
goto :MENU

:SUB_FIX_IDE
echo.
echo ====================================================================
echo    CORRECCION DE DOBLE VENTANA E HISTORIALES EN ANTIGRAVITY IDE
echo ====================================================================
echo.
call :FIND_PYTHON
if not "!PY_CMD!"=="" (
    "!PY_CMD!" "%SCRIPT_DIR%\core\fix_antigravity_ide.py"
    exit /b 0
)

echo [INFO] Aplicando configuracion mediante PowerShell (modo fallback)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%\core\fix_antigravity_ide.ps1"
exit /b 0


:OPT_BRANCH
call :FIND_PYTHON
if not "!PY_CMD!"=="" (
    if "%~2"=="" (
        "!PY_CMD!" "%SCRIPT_DIR%\core\branch_manager.py"
    ) else (
        "!PY_CMD!" "%SCRIPT_DIR%\core\branch_manager.py" switch "%~2"
    )
    goto :END
)
echo [!] Se requiere Python para gestionar ramas.
goto :END

:OPT_BRANCHES
call :FIND_PYTHON
if not "!PY_CMD!"=="" (
    "!PY_CMD!" "%SCRIPT_DIR%\core\branch_manager.py"
    if not "%~1"=="" goto :END
    pause
    goto :MENU
)
echo [!] Se requiere Python para gestionar ramas.
if not "%~1"=="" goto :END
pause
goto :MENU

:OPT_DOCS
call :FIND_PYTHON
if not "!PY_CMD!"=="" (
    "!PY_CMD!" "%SCRIPT_DIR%\core\branch_manager.py" doc
    if not "%~1"=="" goto :END
    pause
    goto :MENU
)
type "%SCRIPT_DIR%\docs\branches_and_books_status.md"
if not "%~1"=="" goto :END
pause
goto :MENU

:END
exit /b 0

:: ====================================================================
:: SUBRUTINA: BUSCADOR DE PYTHON ROBUSTO
:: ====================================================================
:FIND_PYTHON
set "PY_CMD="

if exist "%PROJECT_DIR%\.venv\Scripts\python.exe" (
    set "PY_CMD=%PROJECT_DIR%\.venv\Scripts\python.exe"
    exit /b 0
)
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
if exist "%ProgramFiles%\Python311\python.exe" (
    set "PY_CMD=%ProgramFiles%\Python311\python.exe"
    exit /b 0
)
py -3 -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=py -3"
    exit /b 0
)
python -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
    exit /b 0
)
set "PY_CMD="
exit /b 1
