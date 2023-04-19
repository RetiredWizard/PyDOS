@echo off
pexec import time
pexec envVars['_Year']=time.localtime()[0]
pexec envVars['_Year']=envVars['_Year']>=2023
if %_Year% == True goto done
ntpdate -4
rem reboot so PyDOS starts without memory overhead of ntpdate
reboot

:done
set _Year =
