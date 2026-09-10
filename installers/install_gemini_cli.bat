@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title INSTALADOR DE GEMINI CLI (ANTIGRAVITY CLI / AGY)

echo ====================================================================
echo      VERIFICADOR E INSTALADOR DE GEMINI CLI [AGY]
echo ====================================================================
echo.

:: 1. Comprobar si agy ya esta en PATH o instalado en AppData
set "AGY_CMD="

where.exe agy >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "AGY_CMD=agy"
    echo [OK] Gemini CLI [agy] detectado en PATH.
    goto :SUCCESS
)

if exist "%LOCALAPPDATA%\antigravity-cli\bin\agy.exe" (
    set "AGY_CMD=%LOCALAPPDATA%\antigravity-cli\bin\agy.exe"
    set "PATH=%LOCALAPPDATA%\antigravity-cli\bin;%PATH%"
    echo [OK] Gemini CLI [agy] detectado en %LOCALAPPDATA%\antigravity-cli\bin\
    goto :SUCCESS
)

if exist "%LOCALAPPDATA%\agy\bin\agy.exe" (
    set "AGY_CMD=%LOCALAPPDATA%\agy\bin\agy.exe"
    set "PATH=%LOCALAPPDATA%\agy\bin;%PATH%"
    echo [OK] Gemini CLI [agy] detectado en %LOCALAPPDATA%\agy\bin\
    goto :SUCCESS
)

echo [!] Gemini CLI [agy] no detectado en el sistema.
echo Procediendo a descargar e instalar Gemini CLI oficial...
echo.

:: 2. Ejecutar instalador oficial de PowerShell
powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; irm https://antigravity.google/cli/install.ps1 | iex"

:: 3. Verificar instalacion y registrar en PATH
set "AGY_BIN="
if exist "%LOCALAPPDATA%\antigravity-cli\bin\agy.exe" (
    set "AGY_BIN=%LOCALAPPDATA%\antigravity-cli\bin"
    set "AGY_CMD=%LOCALAPPDATA%\antigravity-cli\bin\agy.exe"
) else if exist "%LOCALAPPDATA%\agy\bin\agy.exe" (
    set "AGY_BIN=%LOCALAPPDATA%\agy\bin"
    set "AGY_CMD=%LOCALAPPDATA%\agy\bin\agy.exe"
)

if not "%AGY_BIN%"=="" (
    set "PATH=%AGY_BIN%;%PATH%"
    powershell -NoProfile -Command "$b = '%AGY_BIN%'; $u = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($u -notlike '*' + $b + '*') { [Environment]::SetEnvironmentVariable('Path', ($u.TrimEnd(';') + ';' + $b), 'User') }" >nul 2>nul
    echo.
    echo [OK] Gemini CLI [agy] instalado exitosamente en:
    echo      %AGY_BIN%
    goto :SUCCESS
)

echo [ERROR] No se pudo confirmar la instalacion de Gemini CLI.
echo Puedes instalarlo manualmente en PowerShell con:
echo   irm https://antigravity.google/cli/install.ps1 ^| iex
if /i not "%~1"=="--nopause" pause
exit /b 1

:SUCCESS
echo.
echo ====================================================================
echo  [OK] GEMINI CLI [AGY] LISTO PARA USAR!
echo ====================================================================
echo  Comandos disponibles:
echo    agy                           : Interfaz CLI interactiva
echo    agyd                          : agy --dangerously-skip-permissions
echo    agy-yolo                      : agy --dangerously-skip-permissions
echo    agy-skip                      : agy --dangerously-skip-permissions
echo ====================================================================
if /i not "%~1"=="--nopause" pause
exit /b 0