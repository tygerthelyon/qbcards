@echo off
title StockFisher
cd /d "%~dp0"
if not exist "runtime\python.exe" goto :not_extracted
"runtime\python.exe" -c "from qbr import store; raise SystemExit(0 if store.meta('synced') else 1)" >nul 2>&1
if errorlevel 1 goto :first_run
:start
echo Starting StockFisher. It opens in your browser.
echo Leave this window open while you use it. Close it to quit.
echo.
"runtime\python.exe" -m qbr.app || pause
exit /b

:first_run
echo First start: StockFisher downloads every question set from QBReader into this folder.
echo That is about 900 MB and takes around 10 to 20 minutes. Only the first start does this.
echo If it is interrupted, double-click Start StockFisher again to pick up where it stopped.
echo.
"runtime\python.exe" -m qbr sync
if errorlevel 1 (
    echo.
    echo The download did not finish. Check your internet connection and run Start StockFisher again.
    pause
    exit /b 1
)
echo.
goto :start

:not_extracted
echo StockFisher has to run from the extracted folder, not from inside the ZIP.
echo.
echo Right-click QBCards-Windows.zip, choose Extract All, open the QBCards folder,
echo then double-click Start StockFisher again.
echo.
pause
