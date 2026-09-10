@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title WINDOWS SCRIPTS - Instalador y Gestor de Herramientas

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_DIR=%SCRIPT_DIR%\..\epub-generator"

set "PY_CMD=python"
if exist "%PROJECT_DIR%\.venv\Scripts\python.exe" (
    set "PY_CMD=%PROJECT_DIR%\.venv\Scripts\python.exe"
)

if /i "%~1"=="--all" goto :OPT_ALL
if /i "%~1"=="--deps" goto :OPT_DEPS
if /i "%~1"=="--brave" goto :OPT_BRAVE
if /i "%~1"=="--git" goto :OPT_GIT
if /i "%~1"=="--aliases" goto :OPT_ALIASES
if /i "%~1"=="--alias" goto :OPT_ALIASES
if /i "%~1"=="--export-aliases" goto :OPT_EXPORT_ALIASES
if /i "%~1"=="--list-aliases" goto :OPT_LIST_ALIASES
if /i "%~1"=="--clean-locks" goto :OPT_CLEAN_LOCKS
if /i "%~1"=="--unlock" goto :OPT_CLEAN_LOCKS
if /i "%~1"=="--agent" goto :OPT_AGENT

:MENU
cls
echo ====================================================================
echo             GESTOR DE SCRIPTS DE WINDOWS (WINDOWS-SCRIPTS)
echo ====================================================================
echo.
echo  [1] Instalar dependencias de epub-generator (Python, .venv y librerias)
echo  [2] Instalar o verificar Brave Browser (Requerido para traducciones)
echo  [3] Instalar o verificar Git para Windows
echo  [4] Configurar o importar todos los alias (orch, unlock, ag, epub...)
echo  [5] Realizar TODO (Git + Brave + Deps + Alias) [Para equipo nuevo]
echo  [6] Limpiar archivos de bloqueo huerfanos (.lock) del orquestador
echo  [7] Crear un nuevo alias y guardarlo en el repositorio
echo  [8] Exportar / Sincronizar alias locales hacia el repositorio
echo  [9] Iniciar Agent Bridge (Discord, auditoria paso a paso, guardia)
echo  [10] Salir
echo.
echo ====================================================================
set /p "CHOICE=Selecciona una opcion [1-10]: "

if "%CHOICE%"=="1" goto :OPT_DEPS
if "%CHOICE%"=="2" goto :OPT_BRAVE
if "%CHOICE%"=="3" goto :OPT_GIT
if "%CHOICE%"=="4" goto :OPT_ALIASES
if "%CHOICE%"=="5" goto :OPT_ALL
if "%CHOICE%"=="6" goto :OPT_CLEAN_LOCKS
if "%CHOICE%"=="7" goto :OPT_ADD_CUSTOM
if "%CHOICE%"=="8" goto :OPT_EXPORT_ALIASES
if "%CHOICE%"=="9" goto :OPT_AGENT
if "%CHOICE%"=="10" goto :END
echo.
echo [!] Opcion invalida.
timeout /t 2 >nul
goto :MENU

:OPT_ALL
call "%SCRIPT_DIR%\installers\install_git.bat" --nopause
call "%SCRIPT_DIR%\installers\install_brave.bat" --nopause
call "%SCRIPT_DIR%\installers\install_epub_deps.bat"
call "%SCRIPT_DIR%\core\configure_cmd_aliases.bat" --nopause
goto :END

:OPT_DEPS
call "%SCRIPT_DIR%\installers\install_epub_deps.bat"
goto :END

:OPT_BRAVE
call "%SCRIPT_DIR%\installers\install_brave.bat"
if not "%~1"=="" goto :END
goto :MENU

:OPT_GIT
call "%SCRIPT_DIR%\installers\install_git.bat"
if not "%~1"=="" goto :END
goto :MENU

:OPT_ALIASES
call "%SCRIPT_DIR%\core\configure_cmd_aliases.bat"
if not "%~1"=="" goto :END
goto :MENU

:OPT_EXPORT_ALIASES
echo.
"%PY_CMD%" "%SCRIPT_DIR%\core\alias_manager.py" export
if not "%~1"=="" goto :END
pause
goto :MENU

:OPT_LIST_ALIASES
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

:END
exit /b 0
