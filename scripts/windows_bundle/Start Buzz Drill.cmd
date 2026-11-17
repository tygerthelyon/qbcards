@echo off
title Buzz Drill
cd /d "%~dp0"
if not exist "runtime\python.exe" goto :not_extracted
"runtime\python.exe" update.py
echo Starting Buzz Drill. It opens in its own window.
echo Leave this window open while you play. Close it to quit.
echo.
"runtime\python.exe" drill_server.py --open || pause
exit /b

:not_extracted
echo Buzz Drill has to run from the extracted folder, not from inside the ZIP.
echo.
echo Right-click QBCards-Windows.zip, choose Extract All, open the QBCards folder,
echo then double-click Start Buzz Drill again.
echo.
pause
