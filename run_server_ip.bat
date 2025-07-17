@echo off
cd /d "%~dp0"
echo Starting Django server on 0.0.0.0:8000...
.\env\Scripts\python manage.py runserver 0.0.0.0:8000
