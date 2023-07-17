@echo off

: close all chrome and cmd instances
taskkill /f /im chrome.exe
taskkill /f /im chromedriver.exe
taskkill /f /im cmd.exe /fi "pid ne %%"

echo Syncing local repository with GitHub...
cd C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards
git pull
ping 127.0.0.1 -n 5 > nul

echo Running automation script...
start "" cmd /c "C:\Users\dashboard-kiosk\AppData\Local\Programs\Python\Python311\python.exe C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards\monitor2.py"
start "" cmd /c "C:\Users\dashboard-kiosk\AppData\Local\Programs\Python\Python311\python.exe C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards\monitor1-window1.py"
start "" cmd /c "C:\Users\dashboard-kiosk\AppData\Local\Programs\Python\Python311\python.exe C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards\monitor1-window2.py"

