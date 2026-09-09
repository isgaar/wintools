@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title CONFIGURAR ALIAS ESTILO LINUX EN CMD (WINDOWS)

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_DIR=%SCRIPT_DIR%\..\epub-generator"
set "BIN_DIR=%LOCALAPPDATA%\Programs\Antigravity IDE\bin"
set "AUTORUN_BAT=%USERPROFILE%\cmd_aliases.bat"

echo ====================================================================
echo      CONFIGURACION DE ALIAS ESTILO LINUX PARA CMD Y POWERSHELL
echo ====================================================================
echo.

:: 1. Crear el archivo de macros persistentes para CMD
echo [1/4] Creando archivo de macros en %AUTORUN_BAT%...
(
    echo @echo off
    echo :: ====================================================================
    echo :: Macros y Alias estilo Linux para CMD ^(Cargados automaticamente^)
    echo :: ====================================================================
    echo doskey ag=antigravity-ide $*
    echo doskey ag.=antigravity-ide .
    echo doskey agy=antigravity-ide $*
    echo doskey antigravity=antigravity-ide $*
    echo doskey epub=cd /d "%PROJECT_DIR%" $T antigravity-ide .
    echo doskey epub-generator=cd /d "%PROJECT_DIR%" $T antigravity-ide .
    echo doskey alias=doskey $*
    echo doskey ls=dir /b /o:gn $*
    echo doskey ll=dir /o:gn $*
    echo doskey clear=cls
    echo doskey which=where.exe $*
) > "%AUTORUN_BAT%"
echo [OK] Archivo %AUTORUN_BAT% creado.

:: 2. Configurar AutoRun en el Registro de Windows
echo [2/4] Registrando AutoRun en HKCU\Software\Microsoft\Command Processor...
reg add "HKCU\Software\Microsoft\Command Processor" /v AutoRun /t REG_SZ /d "\"%AUTORUN_BAT%\"" /f >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] AutoRun registrado. Cada nueva ventana de CMD tendra los alias activos.
) else (
    echo [!] No se pudo escribir en el registro. Se usaran los comandos ejecutables en PATH.
)

:: 3. Crear ejecutables globales en el PATH (en la carpeta bin de Antigravity IDE)
echo [3/4] Creando scripts ejecutables globales en %BIN_DIR%...
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%" 2>nul

:: Script 'ag.cmd' (permite escribir "ag ." o simplemente "ag" para abrir la carpeta actual)
(
    echo @echo off
    echo if "%%~1"=="" ^(
    echo     "%%~dp0antigravity-ide.cmd" .
    echo ^) else ^(
    echo     "%%~dp0antigravity-ide.cmd" %%*
    echo ^)
) > "%BIN_DIR%\ag.cmd"

:: Script 'epub.cmd' (abre el proyecto epub-generator desde cualquier CMD)
(
    echo @echo off
    echo cd /d "%PROJECT_DIR%"
    echo call "%%~dp0antigravity-ide.cmd" .
) > "%BIN_DIR%\epub.cmd"

:: Script 'add-alias.cmd' (herramienta para agregar cualquier carpeta como alias en CMD)
(
    echo @echo off
    echo setlocal
    echo chcp 65001 ^>nul
    echo if "%%~1"=="" ^(
    echo     echo [ERROR] Debes especificar el nombre del alias.
    echo     echo.
    echo     echo Uso:
    echo     echo   add-alias ^^^<nombre^^^> [ruta_de_carpeta]
    echo     echo.
    echo     echo Ejemplos:
    echo     echo   add-alias mimi "C:\Ruta\MiCarpeta"
    echo     echo   add-alias mimi       ^^(asigna la carpeta actual^^)
    echo     exit /b 1
    echo ^)
    echo set "ALIAS_NAME=%%~1"
    echo set "TARGET_DIR=%%~2"
    echo if "!TARGET_DIR!"=="" set "TARGET_DIR=%%CD%%"
    echo set "TARGET_FILE=%BIN_DIR%\!ALIAS_NAME!.cmd"
    echo ^(
    echo     echo @echo off
    echo     echo cd /d "!TARGET_DIR!"
    echo     echo call "%%%%~dp0antigravity-ide.cmd" .
    echo ^) ^> "!TARGET_FILE!"
    echo ====================================================================
    echo  [OK] Alias '!ALIAS_NAME!' creado exitosamente!
    echo ====================================================================
    echo Ahora puedes escribir '!ALIAS_NAME!' desde cualquier CMD para abrir:
    echo   !TARGET_DIR!
    echo directamente en Antigravity IDE.
    echo ====================================================================
) > "%BIN_DIR%\add-alias.cmd"

echo [OK] Comandos globales creados: 'ag', 'epub', 'add-alias'.

:: 4. Configurar PowerShell Profile
echo [4/4] Sincronizando configuracion con PowerShell Profile...
powershell -NoProfile -Command "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force; $p = Split-Path -Parent $PROFILE; if (-not (Test-Path $p)) { New-Item -ItemType Directory -Path $p -Force | Out-Null }; $c = 'function ag { param(`$p = \".\") & \"antigravity-ide\" `$p }; function epub { Set-Location \"%PROJECT_DIR%\"; & \"antigravity-ide\" . }; Set-Alias -Name clear -Value Clear-Host -Option AllScope -ErrorAction SilentlyContinue'; if (Test-Path $PROFILE) { if ((Get-Content $PROFILE -Raw) -notmatch 'antigravity-ide') { Add-Content -Path $PROFILE -Value \"`n`$c\" } } else { Set-Content -Path $PROFILE -Value `$c -Encoding UTF8 }" >nul 2>nul
echo [OK] PowerShell profile configurado.

echo.
echo ====================================================================
echo                   CONFIGURACION FINALIZADA
echo ====================================================================
echo.
echo  ALIAS LISTOS PARA USAR DESDE CUALQUIER TERMINAL CMD:
echo.
echo  1. 'ag .'              : Abre la carpeta actual en Antigravity IDE.
echo  2. 'ag'                : Abre la carpeta actual directamente.
echo  3. 'antigravity-ide .' : Comando oficial completo.
echo  4. 'epub'              : Salta a epub-generator y lo abre en el editor.
echo  5. 'add-alias <nombre> [ruta]' : Crea un alias para cualquier carpeta!
echo.
echo  Comandos estilo Linux integrados en CMD:
echo  - 'ls' / 'll'          : Listar archivos
echo  - 'clear'              : Limpiar terminal (cls)
echo  - 'which <comando>'    : Ver ruta de un ejecutable
echo  - 'alias nombre=cmd'   : Crear alias temporal
echo.
echo ====================================================================
pause
exit /b 0
