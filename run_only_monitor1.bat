@echo off

: close all chrome and cmd instances
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im chromedriver.exe >nul 2>&1
taskkill /f /im cmd.exe /fi "pid ne %%" >nul 2>&1

echo Syncing local repository with GitHub...
cd C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards
git pull
ping 127.0.0.1 -n 5 > nul

echo Running automation script...
start "" cmd /k "C:\Users\dashboard-kiosk\AppData\Local\Programs\Python\Python311\python.exe C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards\monitor1-window1.py"
start "" cmd /k "C:\Users\dashboard-kiosk\AppData\Local\Programs\Python\Python311\python.exe C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards\monitor1-window2.py"

