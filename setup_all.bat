@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title WINDOWS SCRIPTS - Instalador y Gestor de Herramientas

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

if /i "%~1"=="--all" goto :OPT_ALL
if /i "%~1"=="--deps" goto :OPT_DEPS
if /i "%~1"=="--aliases" goto :OPT_ALIASES
if /i "%~1"=="--alias" goto :OPT_ALIASES
if /i "%~1"=="--git" goto :OPT_GIT

:MENU
cls
echo ====================================================================
echo             GESTOR DE SCRIPTS DE WINDOWS (WINDOWS-SCRIPTS)
echo ====================================================================
echo.
echo  [1] Instalar dependencias de epub-generator (Crea .venv e instala librerias)
echo  [2] Configurar alias estilo Linux en CMD (ag ., epub, add-alias...)
echo  [3] Instalar o verificar Git para Windows
echo  [4] Realizar TODO (Git + Dependencias + Alias CMD) [Recomendado]
echo  [5] Crear un nuevo alias para una carpeta personalizada
echo  [6] Salir
echo.
echo ====================================================================
set /p "CHOICE=Selecciona una opcion [1-6]: "

if "%CHOICE%"=="1" goto :OPT_DEPS
if "%CHOICE%"=="2" goto :OPT_ALIASES
if "%CHOICE%"=="3" goto :OPT_GIT
if "%CHOICE%"=="4" goto :OPT_ALL
if "%CHOICE%"=="5" goto :OPT_ADD_CUSTOM
if "%CHOICE%"=="6" goto :END
echo.
echo [!] Opcion invalida.
timeout /t 2 >nul
goto :MENU

:OPT_ALL
call "%SCRIPT_DIR%\install_git.bat" --nopause
call "%SCRIPT_DIR%\install_epub_deps.bat"
call "%SCRIPT_DIR%\configurar_aliases_cmd.bat"
goto :END

:OPT_DEPS
call "%SCRIPT_DIR%\install_epub_deps.bat"
goto :END

:OPT_ALIASES
call "%SCRIPT_DIR%\configurar_aliases_cmd.bat"
goto :END

:OPT_GIT
call "%SCRIPT_DIR%\install_git.bat"
goto :MENU

:OPT_ADD_CUSTOM
cls
echo ====================================================================
echo      CREAR ALIAS PERSONALIZADO PARA UNA CARPETA EN CMD
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

set "BIN_DIR=%LOCALAPPDATA%\Programs\Antigravity IDE\bin"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%" 2>nul
(
    echo @echo off
    echo cd /d "%NEW_PATH%"
    echo call "%%~dp0antigravity-ide.cmd" .
) > "%BIN_DIR%\%NEW_NAME%.cmd"

echo.
echo ====================================================================
echo  [OK] Alias '%NEW_NAME%' creado exitosamente!
echo ====================================================================
echo Ahora puedes escribir '%NEW_NAME%' en cualquier terminal CMD para abrir:
echo %NEW_PATH%
echo directamente en Antigravity IDE.
echo ====================================================================
pause
goto :MENU

:END
exit /b 0
