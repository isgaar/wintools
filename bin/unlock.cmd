@echo off
setlocal
set "BIN_DIR=%~dp0"
set "ROOT_DIR=%BIN_DIR%.."
set "STATE_DIR=%ROOT_DIR%\..\epub-generator\amazon_publisher\translator\orchestrator\state"
if exist "%STATE_DIR%" (
    del /f /q "%STATE_DIR%\*.lock" 2>nul
    echo [OK] Archivos .lock eliminados de %STATE_DIR%
) else (
    echo [!] Carpeta de estado no encontrada: %STATE_DIR%
)
