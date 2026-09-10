@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title INSTALADOR DE BRAVE BROWSER (TRADUCCIONES GEMINI CDP)

echo ====================================================================
echo      VERIFICADOR E INSTALADOR DE BRAVE BROWSER (GEMINI AUTOMATION)
echo ====================================================================
echo.

set "BRAVE_PATH=C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
set "BRAVE_USER=%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"

:: 1. Comprobar si Brave ya esta instalado en la ruta oficial de 64-bit
if exist "%BRAVE_PATH%" (
    echo [OK] Brave Browser detectado en:
    echo      %BRAVE_PATH%
    goto :SUCCESS
)

if exist "%BRAVE_USER%" (
    echo [OK] Brave Browser detectado en:
    echo      %BRAVE_USER%
    goto :SUCCESS
)

echo [!] Brave Browser no fue detectado en las rutas estandar.
echo Brave es OBLIGATORIO para ejecutar el orquestador de traducciones (gem_browser).
echo.
echo Procediendo a descargar e instalar Brave Browser...
echo.

:: 2. Intentar instalar con winget si esta disponible
where.exe winget >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [1/2] Intentando instalacion silenciosa mediante winget...
    winget install --id Brave.Brave -e --source winget --accept-package-agreements --accept-source-agreements
    if exist "%BRAVE_PATH%" (
        echo [OK] Brave Browser instalado exitosamente con winget!
        goto :SUCCESS
    )
    if exist "%BRAVE_USER%" (
        echo [OK] Brave Browser instalado exitosamente con winget!
        goto :SUCCESS
    )
)

:: 3. Descarga directa oficial de Brave Standalone si winget no esta disponible
echo [2/2] Descargando instalador oficial de Brave Browser (64-bit)...
set "BRAVE_INSTALLER=%TEMP%\BraveBrowserSetup.exe"

powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://laptop-updates.brave.com/latest/winx64' -OutFile '%BRAVE_INSTALLER%'"

if not exist "%BRAVE_INSTALLER%" (
    echo [ERROR] No se pudo descargar el instalador de Brave automaticamente.
    echo Por favor descargalo e instalalo manualmente desde: https://brave.com/
    if /i not "%~1"=="--nopause" pause
    exit /b 1
)

echo Ejecutando instalador silencioso de Brave...
start /wait "" "%BRAVE_INSTALLER%" /silent /install

:: 4. Verificar instalacion final
if exist "%BRAVE_PATH%" (
    echo [OK] Brave Browser instalado correctamente en %BRAVE_PATH%
    goto :SUCCESS
)
if exist "%BRAVE_USER%" (
    echo [OK] Brave Browser instalado correctamente en %BRAVE_USER%
    goto :SUCCESS
)

echo [ERROR] No se pudo confirmar la instalacion de Brave Browser.
echo Por favor asegurate de instalarlo en:
echo C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe
if /i not "%~1"=="--nopause" pause
exit /b 1

:SUCCESS
echo.
echo ====================================================================
echo  [PASO OBLIGATORIO PARA TRADUCIR CON EL ORQUESTADOR]
echo ====================================================================
echo  1. Abre Brave Browser manualmente.
echo  2. Ve a https://gemini.google.com e inicia sesion con tu cuenta.
echo  3. Asegurate de que la sesion permanezca activa.
echo.
echo  El orquestador conectara con este perfil para procesar las
echo  traducciones sin consumir energia en tu maquina principal!
echo ====================================================================
if /i not "%~1"=="--nopause" pause
exit /b 0
