@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title INSTALADOR DE GIT PARA WINDOWS

echo ====================================================================
echo             VERIFICADOR E INSTALADOR DE GIT PARA WINDOWS
echo ====================================================================
echo.

:: 1. Comprobar si git ya esta en PATH
git --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('git --version') do echo [OK] %%v ya esta instalado en el sistema.
    goto :SUCCESS
)

:: 2. Comprobar rutas estandar comunes
if exist "%ProgramFiles%\Git\cmd\git.exe" (
    set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
    echo [OK] Git encontrado en %ProgramFiles%\Git\cmd\
    goto :SUCCESS
)

if exist "%LOCALAPPDATA%\Programs\Git\cmd\git.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%"
    echo [OK] Git encontrado en %LOCALAPPDATA%\Programs\Git\cmd\
    goto :SUCCESS
)

echo [!] Git no fue detectado en el sistema.
echo Procediendo a descargar e instalar Git para Windows...
echo.

:: 3. Intentar instalar via winget si esta disponible
where.exe winget >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [1/2] Intentando instalacion silenciosa mediante winget...
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
    if exist "%ProgramFiles%\Git\cmd\git.exe" (
        set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
        echo [OK] Git instalado exitosamente con winget!
        goto :SUCCESS
    )
)

:: 4. Descarga directa oficial del instalador de Git de 64 bits si winget falla
echo [2/2] Descargando instalador oficial de Git para Windows (Standalone 64-bit)...
set "GIT_INSTALLER=%TEMP%\Git-Installer.exe"

powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe' -OutFile '%GIT_INSTALLER%'"

if not exist "%GIT_INSTALLER%" (
    echo [ERROR] No se pudo descargar el instalador de Git automaticamente.
    echo Por favor descargalo manualmente desde: https://git-scm.com/download/win
    if /i not "%~1"=="--nopause" pause
    exit /b 1
)

echo Instalando Git silenciosamente (por favor espera)...
start /wait "" "%GIT_INSTALLER%" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"

:: 5. Verificar instalacion final
if exist "%ProgramFiles%\Git\cmd\git.exe" (
    set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
    echo [OK] Git se instalo correctamente en %ProgramFiles%\Git\cmd\
    goto :SUCCESS
)

echo [ERROR] No se pudo confirmar la instalacion de Git.
if /i not "%~1"=="--nopause" pause
exit /b 1

:SUCCESS
echo.
echo ====================================================================
echo  [OK] GIT LISTO PARA USAR EN WINDOWS!
echo ====================================================================
echo Puedes verificar ejecutando: git --version
echo ====================================================================
if /i not "%~1"=="--nopause" pause
exit /b 0
