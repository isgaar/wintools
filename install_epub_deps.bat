@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title EPUB-GENERATOR - Instalador de Dependencias (Sin tocar el repositorio)

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_DIR=%SCRIPT_DIR%\..\epub-generator"
set "VENV_DIR=%PROJECT_DIR%\.venv"
set "PYTHON_CMD="

echo ====================================================================
echo      INSTALADOR DE DEPENDENCIAS PARA EPUB-GENERATOR
echo ====================================================================
echo.
echo Repositorio objetivo: %PROJECT_DIR%
echo.

if not exist "%PROJECT_DIR%" (
    echo [ERROR] No se encontro la carpeta epub-generator en "%PROJECT_DIR%".
    pause
    exit /b 1
)

:: ====================================================================
:: 0. COMPROBAR O INSTALAR GIT
:: ====================================================================
call :CHECK_OR_INSTALL_GIT

:: ====================================================================
:: 1. COMPROBAR O INSTALAR PYTHON 3.11
:: ====================================================================
echo [2/4] Verificando interprete de Python...

:: Probar si python en PATH funciona
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=python"
    for /f "delims=" %%v in ('python -c "import sys; print(sys.version.split()[0])"') do set "PY_VER=%%v"
    echo [OK] Python encontrado: version !PY_VER!
    goto :CREATE_VENV
)

:: Probar en AppData del usuario
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    echo [OK] Python 3.11 encontrado en %LOCALAPPDATA%\Programs\Python\Python311\
    goto :CREATE_VENV
)

:: Probar py launcher
py -3 -c "import sys; sys.exit(0)" 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=py -3"
    echo [OK] Python encontrado via py launcher.
    goto :CREATE_VENV
)

:: Si no existe, descargar e instalar Python 3.11 silenciosamente
echo [!] Python 3.10+ no detectado en el sistema.
echo Descargando e instalando Python 3.11 oficial para el usuario...
set "INSTALLER_PATH=%TEMP%\python-3.11.9-amd64.exe"

if not exist "%INSTALLER_PATH%" (
    echo Descargando python-3.11.9-amd64.exe...
    powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%INSTALLER_PATH%'"
)

echo Ejecutando instalador silencioso...
start /wait "" "%INSTALLER_PATH%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_launcher=0 InstallLauncherAllUsers=0

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%"
    echo [OK] Python 3.11 instalado correctamente!
) else (
    echo [ERROR] No se pudo instalar Python de forma automatica.
    echo Por favor instala Python 3.11 manualmente desde https://www.python.org/
    pause
    exit /b 1
)

:: ====================================================================
:: 2. CREAR / VERIFICAR ENTORNO VIRTUAL (.venv)
:: ====================================================================
:CREATE_VENV
echo.
echo [3/4] Verificando entorno virtual en "%VENV_DIR%"...

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creando entorno virtual .venv...
    "%PYTHON_CMD%" -m venv "%VENV_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Fallo al crear el entorno virtual.
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado exitosamente.
) else (
    echo [INFO] El entorno virtual ya existe.
)

set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"

:: ====================================================================
:: 3. INSTALAR DEPENDENCIAS DE CADA MODULO (SIN TOCAR EL REPOSITORIO)
:: ====================================================================
echo.
echo [4/4] Instalando dependencias de los modulos de epub-generator...
echo Actualizando pip...
"%VENV_PYTHON%" -m pip install --upgrade pip --quiet

if exist "%PROJECT_DIR%\modules\epub_generator\requirements.txt" (
    echo.
    echo -- Instalando: modules/epub_generator/requirements.txt
    "%VENV_PIP%" install -r "%PROJECT_DIR%\modules\epub_generator\requirements.txt"
)

if exist "%PROJECT_DIR%\01translator\requirements.txt" (
    echo.
    echo -- Instalando: 01translator/requirements.txt
    "%VENV_PIP%" install -r "%PROJECT_DIR%\01translator\requirements.txt"
)

if exist "%PROJECT_DIR%\tools\grammar_checker\requirements.txt" (
    echo.
    echo -- Instalando: tools/grammar_checker/requirements.txt
    "%VENV_PIP%" install -r "%PROJECT_DIR%\tools\grammar_checker\requirements.txt"
)

if exist "%PROJECT_DIR%\modules\print-ready-generator\requirements.txt" (
    echo.
    echo -- Instalando: modules/print-ready-generator/requirements.txt
    "%VENV_PIP%" install -r "%PROJECT_DIR%\modules\print-ready-generator\requirements.txt"
)

echo.
echo ====================================================================
echo  [OK] PROCESO COMPLETADO EXITOSAMENTE!
echo ====================================================================
echo Todas las librerias se instalaron en:
echo %VENV_DIR%
echo.
echo Ningun archivo del repositorio epub-generator fue modificado.
echo ====================================================================
pause
exit /b 0

:: ====================================================================
:: SUBRUTINA: COMPROBAR O INSTALAR GIT
:: ====================================================================
:CHECK_OR_INSTALL_GIT
echo [1/4] Verificando instalacion de Git...
git --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%g in ('git --version') do echo [OK] %%g detectado.
    goto :EOF
)

if exist "%ProgramFiles%\Git\cmd\git.exe" (
    set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
    echo [OK] Git encontrado en %ProgramFiles%\Git\cmd\
    goto :EOF
)

if exist "%LOCALAPPDATA%\Programs\Git\cmd\git.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%"
    echo [OK] Git encontrado en %LOCALAPPDATA%\Programs\Git\cmd\
    goto :EOF
)

echo [!] Git no detectado. Procediendo a descargarlo e instalarlo...
if exist "%SCRIPT_DIR%\install_git.bat" (
    call "%SCRIPT_DIR%\install_git.bat" --nopause
) else (
    where.exe winget >nul 2>&1 && winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
)
if exist "%ProgramFiles%\Git\cmd\git.exe" set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
goto :EOF
