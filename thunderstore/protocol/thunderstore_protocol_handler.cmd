@echo off & setlocal EnableDelayedExpansion
set "PATH=%~dp0..\..\plugin_python\dlls;%PATH%"
"%~dp0thunderstore_protocol_handler.exe" %*
if %errorlevel% LSS 0 (
    title %~dp0thunderstore_protocol_handler.exe
    echo MO Python version mismatch^! 1>&2
    set /p version=<"%~dp0.python-version"
    echo Required: !version! 1>&2
    for %%p in ("%~dp0..\..\plugin_python\dlls") do SET "dllPath=%%~fp"
    echo Available in !dllPath!: 1>&2
    dir /b "!dllPath!\python*" 1>&2
    pause
)