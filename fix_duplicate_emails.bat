@echo off
echo Waste Sorter - Fix Duplicate Emails Utility
echo =========================================
echo.

echo Step 1: Checking for duplicate emails in the system...
python manage.py check_duplicate_emails
echo.

echo Step 2: Do you want to fix duplicate emails? (Y/N)
set /p CHOICE="Enter your choice (Y/N): "
if /i "%CHOICE%"=="Y" goto fix_emails
if /i "%CHOICE%"=="y" goto fix_emails
goto end

:fix_emails
echo.
echo Running in dry-run mode first to see what changes would be made...
python manage.py fix_duplicate_emails --dry-run
echo.
echo Are you sure you want to apply these changes? (Y/N)
set /p CONFIRM="Enter your choice (Y/N): "
if /i "%CONFIRM%"=="Y" goto apply_fix
if /i "%CONFIRM%"=="y" goto apply_fix
goto end

:apply_fix
echo.
echo Applying changes to fix duplicate emails...
python manage.py fix_duplicate_emails
echo.
echo Verifying changes...
python manage.py check_duplicate_emails

:end
echo.
echo Utility completed.
pause
