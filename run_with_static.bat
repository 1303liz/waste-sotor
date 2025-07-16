@echo off
echo Collecting static files...
cd %~dp0

REM Check if the virtual environment exists
if not exist ".\env\Scripts\python.exe" (
    echo Virtual environment not found. Please ensure you have set up the environment correctly.
    pause
    exit /b 1
)

REM Collect static files
.\env\Scripts\python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo Error collecting static files.
    pause
    exit /b 1
)

echo.
echo Static files collected successfully.
echo Now starting the server...
echo.

REM Create a directory for logs if it doesn't exist
if not exist "logs" mkdir logs

REM Start the server with output redirection
call run_server.bat > logs\server_output.log 2>&1
