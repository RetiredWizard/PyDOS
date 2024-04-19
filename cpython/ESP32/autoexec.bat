@echo off
pexec from supervisor import runtime
pexec envVars['_RunReason']=runtime.run_reason
rem -4 is timezone offset, default value -4 = Eastern Standard Time
if not %_RunReason% == supervisor.RunReason.STARTUP goto done
getdate
reboot

:done
set _RunReason = 
