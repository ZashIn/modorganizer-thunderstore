@echo off & setlocal EnableDelayedExpansion
pushd %~dp0
set "PATH=%~dp0..\..\plugin_python\dlls;%PATH%"
for %%f in ("..\..\plugin_python\dlls\python31*.dll") do (
    SET "pythonVersion=%%~nf"
)
if exist "thunderstore_protocol_handler_!pythonVersion!.exe" (
    "thunderstore_protocol_handler_!pythonVersion!.exe" %*
) else (
    "thunderstore_protocol_handler.exe" %*
)
if %errorlevel% LSS 0 (
    title %~dp0thunderstore_protocol_handler.exe
    echo MO Python version mismatch^! 1>&2
    echo Protocol handlers in "%cd%": 1>&2
    dir /b "thunderstore_protocol_handler_*.exe"
    for %%p in ("%~dp0..\..\plugin_python\dlls") do SET "dllPath=%%~fp"
    echo Available in !dllPath!: 1>&2
    dir /b "!dllPath!\python31*.dll" 1>&2
    pause
)
