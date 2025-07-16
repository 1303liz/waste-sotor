@echo off
echo Checking network configuration...
echo.

REM Get the IP address using PowerShell
for /f "tokens=*" %%a in ('powershell -command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like '*Ethernet*' -or $_.InterfaceAlias -like '*Wi-Fi*'} | Select-Object -First 1).IPAddress"') do set IP_ADDR=%%a

if "%IP_ADDR%"=="" (
    echo Could not determine IP address automatically.
    set IP_ADDR=YOUR_IP_ADDRESS
) else (
    echo Your IP address is: %IP_ADDR%
)

echo.
echo Checking if port 8000 is open...
netstat -an | find "0.0.0.0:8000"
if %errorlevel% equ 0 (
    echo Port 8000 is already in use. Please close the application using this port and try again.
) else (
    echo Port 8000 is available.
)

echo.
echo Checking firewall status...
netsh advfirewall show allprofiles state

echo.
echo If the firewall is ON, you might need to allow Django through the firewall.
echo To do this, run the following command as Administrator:
echo netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow program="%%USERPROFILE%%\Downloads\waste-sotor\env\Scripts\python.exe" protocol=TCP localport=8000

echo.
echo Ping test to your machine (this will check basic network connectivity):
ping %IP_ADDR% -n 2

echo.
echo Network check complete.
echo If you're still having issues accessing the application from other devices:
echo 1. Make sure your device and the other devices are on the same network
echo 2. Try temporarily disabling the firewall (for testing only)
echo 3. Check if your router has client isolation enabled (this prevents devices from talking to each other)
echo.

pause
