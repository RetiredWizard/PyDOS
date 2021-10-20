@echo off
set _val = %1%
if "x%_val%" == "x" goto prompt
goto copy
:prompt
set/p _val = (U)art or (K)eyboard FeatherWing
:copy
if %_val% == U goto uart
if %_val% == u goto uart
if %_val% == K goto kfw
if %_val% == k goto kfw
goto prompt
:uart
copy pydos_ui_uart.py pydos_ui.py
goto done
:kfw
copy pydos_ui_kfw.py pydos_ui.py
:done
set _val=
