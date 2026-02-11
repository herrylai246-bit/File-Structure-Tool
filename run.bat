@echo off
cd /d "%~dp0"
python file_structure_viewer.py
if errorlevel 1 (
    echo.
    echo Error running the application. Press any key to exit...
    pause
)
