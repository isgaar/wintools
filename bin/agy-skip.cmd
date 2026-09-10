@echo off

where.exe agy >nul 2>&1

if %ERRORLEVEL% NEQ 0 (

    if exist "%LOCALAPPDATA%\antigravity-cli\bin\agy.exe" set "PATH=%LOCALAPPDATA%\antigravity-cli\bin;%PATH%"

    if exist "%LOCALAPPDATA%\agy\bin\agy.exe" set "PATH=%LOCALAPPDATA%\agy\bin;%PATH%"

)

agy --dangerously-skip-permissions %*

