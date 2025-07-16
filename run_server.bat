@echo off
echo Starting Django server...
echo.

REM Get the IP address using PowerShell
for /f "tokens=*" %%a in ('powershell -command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like '*Ethernet*' -or $_.InterfaceAlias -like '*Wi-Fi*'} | Select-Object -First 1).IPAddress"') do set IP_ADDR=%%a

if "%IP_ADDR%"=="" (
    echo Could not determine IP address automatically.
    set IP_ADDR=YOUR_IP_ADDRESS
)

echo The server will be accessible at:
echo - Local:   http://127.0.0.1:8000
echo - Network: http://%IP_ADDR%:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

cd %~dp0

REM Check if the virtual environment exists
if not exist ".\env\Scripts\python.exe" (
    echo Virtual environment not found. Please ensure you have set up the environment correctly.
    pause
    exit /b 1
)

REM Check if manage.py exists
if not exist "manage.py" (
    echo manage.py not found. Please ensure you are in the correct directory.
    pause
    exit /b 1
)

REM Start the Django server
echo Starting server on 0.0.0.0:8000...
.\env\Scripts\python manage.py runserver 0.0.0.0:8000
