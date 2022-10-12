@echo off
pexec from sys import implementation
pexec envVars['_implementation']=implementation.name.upper()
if %_implementation% == CIRCUITPYTHON goto cpython
if %_implementation% == MICROPYTHON goto mpython
goto done

:cpython
pexec from supervisor import runtime
pexec envVars['_RunReason']=runtime.run_reason
rem -4 is timezone offset, default value -4 = Eastern Standard Time
if %_RunReason% == supervisor.RunReason.STARTUP ntpdate -4
set _RunReason =
goto done

:mpython
ntpdate -4

:done
set _implementation = 
