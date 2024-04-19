@echo off
pexec import time
pexec envVars['_Year']=time.localtime()[0]
pexec envVars['_Year']=envVars['_Year']>=2023
if %_Year% == True goto done
getdate
if not %errorlevel% == 0 goto done
rem reboot so PyDOS starts without memory overhead of ntpdate
reboot

:done
set _Year =
