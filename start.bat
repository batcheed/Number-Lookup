@echo off
title TOOL by @batcheed
color 0a
setlocal

set "x=1"
set "y=2"
set "z=3"

:menu
cls
echo ================================
echo          TOOL MENU
echo ================================
echo [%x%] Run program
echo [%y%] Support (Discord)
echo [%z%] Exit
echo ================================
set /p opt=Choose an option:

if "%opt%"=="%x%" goto run
if "%opt%"=="%y%" goto support
if "%opt%"=="%z%" goto exit
goto menu

:run
cls
echo Installing requirements...
pip install -r requirements.txt >nul 2>&1
echo Starting main.py...
python main.py
pause
goto menu

:support
start https://discord.gg/fFfKUbGdkD
goto menu

:exit
echo Exiting...
exit
