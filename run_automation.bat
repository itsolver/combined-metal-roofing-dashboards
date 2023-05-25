@echo off

echo Syncing local repository with GitHub...
cd C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards
git pull

echo Running automation script...
start "" cmd /c "C:\Users\dashboard-kiosk\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards\monitor1.py"
start "" cmd /c "C:\Users\dashboard-kiosk\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\dashboard-kiosk\AppData\Roaming\combined-metal-roofing-dashboards\monitor2.py"
