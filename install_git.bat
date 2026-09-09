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

:: 4. Fallback: Descarga directa oficial del instalador de Git de GitHub Releases
echo [2/2] Descargando instalador oficial de Git para Windows...
set "GIT_INSTALLER=%TEMP%\Git-Installer-64bit.exe"

powershell -NoProfile -Command "$url = (Invoke-RestMethod -Uri 'https://api.github.com/repos/git-for-windows/git/releases/latest').assets | Where-Object { $_.name -match '64-bit\.exe$' -and $_.name -notmatch 'MinGit|PortableGit' } | Select-Object -First 1 -ExpandProperty browser_download_url; if (-not $url) { $url = 'https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe' }; Write-Host \"Descargando desde: $url\"; Invoke-WebRequest -Uri $url -OutFile '%GIT_INSTALLER%'"

if not exist "%GIT_INSTALLER%" (
    echo [ERROR] No se pudo descargar el instalador de Git.
    echo Por favor descargalo manualmente desde https://git-scm.com/
    pause
    exit /b 1
)

echo Instalando Git silenciosamente...
start /wait "" "%GIT_INSTALLER%" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS

if exist "%ProgramFiles%\Git\cmd\git.exe" (
    set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
    echo [OK] Git para Windows instalado exitosamente!
    goto :SUCCESS
) else if exist "%LOCALAPPDATA%\Programs\Git\cmd\git.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%"
    echo [OK] Git para Windows instalado exitosamente!
    goto :SUCCESS
) else (
    echo [!] La instalacion finalizo. Si la consola no reconoce 'git',
    echo reinicia la ventana de CMD para actualizar las variables de entorno.
)

:SUCCESS
echo.
echo ====================================================================
echo  [OK] Git esta listo para usarse.
echo ====================================================================
if "%~1"=="--nopause" goto :EOF
if "%~1"=="/nopause" goto :EOF
pause
exit /b 0
