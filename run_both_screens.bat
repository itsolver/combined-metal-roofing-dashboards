@echo off

: close all chrome and cmd instances
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im chromedriver.exe >nul 2>&1
taskkill /f /im cmd.exe /fi "pid ne %%" >nul 2>&1

echo Syncing local repository with GitHub...
cd C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards
git pull
git checkout run_both_screens.bat
git checkout monitor1-window1.py
git checkout monitor1-window2.py
git checkout monitor2.py
git checkout requirements.txt
ping 127.0.0.1 -n 5 > nul

echo Cleaning up and updating ChromeDriver...
del /f /q chromedriver.exe >nul 2>&1
env\Scripts\python.exe -c "from webdriver_manager.chrome import ChromeDriverManager, ChromeType; ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()"

echo Running automation script...
start "" cmd /k "env\Scripts\python.exe monitor2.py"
start "" cmd /k "env\Scripts\python.exe monitor1-window1.py"
start "" cmd /k "env\Scripts\python.exe monitor1-window2.py"
