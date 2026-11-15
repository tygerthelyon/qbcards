@echo off
cd /d "%~dp0"
where pyw >nul 2>&1
if errorlevel 1 (
    echo StockFisher needs Python 3.9 or later with the Windows Python launcher.
    echo After installing Python, reopen this shortcut.
    pause
    exit /b 1
)
py -3.9 -c "" >nul 2>&1
if not errorlevel 1 (
    start "" pyw -3.9 "%~dp0launch_stockfisher.pyw"
) else (
    start "" pyw -3 "%~dp0launch_stockfisher.pyw"
)
