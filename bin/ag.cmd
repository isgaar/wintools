@echo off

where.exe antigravity-ide >nul 2>&1

if %ERRORLEVEL% EQU 0 (

    if "%~1"=="" (

        call antigravity-ide . 2>nul

    ) else (

        call antigravity-ide %* 2>nul

    )

) else (

    if "%~1"=="" (

        explorer .

    ) else (

        if exist "%~1" (

            cd /d "%~1"

        ) else (

            explorer .

        )

    )

)

