@echo off & setlocal
set "PATH=%~dp0..\..\plugin_python\dlls;%PATH%"
"%~dp0thunderstore_protocol_handler.exe" %*