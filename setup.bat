@echo off
del /README.md
pexec from sys import implementation
pexec envVars["_implementation"] = implementation.name.upper()
if %_implementation% == CIRCUITPYTHON set _ans = C
if %_implementation% == MICROPYTHON set _ans = M
if %_ans% == M goto mpython

:cpython
copy/y /cpython/* /
if not exist /lib mkdir /lib
copy /cpython/lib/* /lib/
pexec/q import adafruit_bus_device
if errorlevel 0 goto bus_device_builtin
echo copy /mpython/lib/optional/adafruit_bus_device /lib/
if not exist /lib/adafruit_bus_device mkdir /lib/adafruit_bus_device
copy /cpython/lib/optional/adafruit_bus_device/* /lib/adafruit_bus_device/
:bus_device_builtin
pexec import board
pexec envVars["_boardID"] = board.board_id
pexec/q import sdcardio
if not errorlevel 0 echo copy /cpython/lib/optional/adafruit_sdcard.mpy /lib/
if not errorlevel 0 copy /cpython/lib/optional/adafruit_sdcard.mpy /lib/
if "%_boardID%" == "teensy41" echo copy/y /cpython/lib/optional/adafruit_sdcard.mpy /lib/
if "%_boardID%" == "teensy41" copy/y /cpython/lib/optional/adafruit_sdcard.mpy /lib/
pexec/q import neopixel
if not errorlevel 0 echo copy /cpython/lib/optional/neopixel.mpy /lib/
if not errorlevel 0 copy /cpython/lib/optional/neopixel.mpy /lib/
if exist /cpython/boardconfigs/pydos_bcfg_%_boardID%.py goto foundbcfgCP
echo *** Warning *** No board configuration file found
echo *** Warning *** /cpython/boardconfigs/pydos_bcfg_%_boardID%.py
goto board
:foundbcfgCP
echo copy /cpython/boardconfigs/pydos_bcfg_%_boardID%.py to /lib/pydos_bcfg.py
copy/y /cpython/boardconfigs/pydos_bcfg_%_boardID%.py /lib/pydos_bcfg.py
goto board

:mpython
if exist /setup.bat goto flashmountedroot
if not exist /sdcard goto flashmountedroot
if exist /sdcard/boot.py rename /sdcard/boot.py /sdcard/boot.pydos
if exist /sdcard/main.py rename /sdcard/main.py /sdcard/main.pydos
echo copy /flash/boot.py /sdcard/boot.py
copy/y /flash/boot.py /sdcard/boot.py
echo copy /flash/mpython/main.py /sdcard/main.py
copy/y /flash/mpython/main.py /sdcard/main.py
echo .
echo *** Power Cycle the board and run setup again....  ***
echo .
exit
:flashmountedroot
copy/y /mpython/* /
if not exist /lib mkdir /lib
copy /mpython/lib/* /lib/
pexec/q import neopixel
rem if not errorlevel 0 echo copy /mpython/lib/optional/ws2812.py /lib/
rem if not errorlevel 0 copy /mpython/lib/optional/ws2812.py /lib/
if not errorlevel 0 echo copy /mpython/lib/optional/neopixel.py /lib/
if not errorlevel 0 copy /mpython/lib/optional/neopixel.py /lib/
pexec envVars["_uname"] = implementation._machine
if not "%_uname%" == "Sparkfun SAMD51 Thing Plus with SAMD51J20A" goto skip_SAMD51
if not exist /lib mkdir /lib
copy /mpython/extFlash/lib/* /lib/
del /lib/XIAO_nRF52840.py
:skip_SAMD51
if not "%_uname%" == "XIAO nRF52840 Sense with nRF52840" goto skip_nRF
if not exist /lib mkdir /lib
copy /mpython/extFlash/lib/* /lib/
del /lib/ThngPls_SAMD51.py
:skip_nRF
if exist "/mpython/boardconfigs/pydos_bcfg_%_uname%.py" goto foundbcfg
echo *** Warning *** No board configuration file found:
echo   /mpython/boardconfigs/pydos_bcfg_%_uname%.py
goto board
:foundbcfg
echo copy "/mpython/boardconfigs/pydos_bcfg_%_uname%.py" to /lib/pydos_bcfg.py
copy/y "/mpython/boardconfigs/pydos_bcfg_%_uname%.py" /lib/pydos_bcfg.py

:board
echo .
echo (N)anoConnect, (E) ESP32[C3/D4/S2/S3...] or (E) Pico-W board,
set/p _ans2 = (O)ther RP2040/STM32/Atmel SAMD/nRF/ARM Cortex-M board:
if %_ans2% == N goto nanoconnect
if %_ans2% == n goto nanoconnect
if %_ans2% == e goto esp32
if %_ans2% == E goto esp32
if %_ans2% == o goto other
if %_ans2% == O goto other
echo Invalid selection (N,E or O)
goto board

:nanoconnect
set _ans2 = N
if %_ans% == C goto nanoconnectCP
if not exist /lib mkdir /lib
copy /mpython/NanoConnect/lib/* /lib/
goto esp32MP

:nanoconnectCP
if exist /wifi_test.py del wifi_test.py
echo copy /cpython/ESP32/autoexec.bat /
copy /cpython/ESP32/autoexec.bat /
if not exist /lib mkdir /lib
copy /cpython/NanoConnect/lib/* /lib/
if not exist /lib/adafruit_esp32spi mkdir /lib/adafruit_esp32spi
copy /cpython/NanoConnect/lib/adafruit_esp32spi/* /lib/adafruit_esp32spi/
goto wifienv

:esp32
if %_ans2% == e set _ans2 = E
if %_ans% == M goto esp32MP
copy/y /cpython/ESP32/* /
if not exist /lib mkdir /lib
copy /cpython/ESP32/lib/* /lib/
goto other

:esp32MP
copy /mpython/ESP32/* /
pexec/q import urequests
if not errorlevel 0 echo copy /mpython/lib/optional/urequests.py /lib/
if not exist /lib mkdir /lib
if not errorlevel 0 copy /mpython/lib/optional/urequests.py /lib/

:other
if %_ans2% == N goto wifienv
if %_ans2% == o set _ans2 = O
if "%_boardID%" == "raspberry_pi_pico_w" goto copy_code
rem Feather Huzzah may need the sound pin mod but doesn't have the memory to spare
if "%_boardID%" == "adafruit_feather_huzzah32" del /autoexec.bat
if "%_boardID%" == "adafruit_feather_huzzah32" del /boot.py
if "%_boardID%" == "adafruit_feather_huzzah32" goto copy_code
if "%_boardID%" == "matrixportal_m4" goto copy_code
if %_ans2% == E goto skip_codecopy
if exist /lib/pydos_wifi.py del /lib/pydos_wifi.py
if exist /ntpdate.py del /ntpdate.py
del /wifi_*.py
goto skip_codecopy
:copy_code
echo copy /cpython/code.py /
copy/y /cpython/code.py /
echo copy /cpython/main.py /
copy/y /cpython/main.py /
:skip_codecopy
if %_ans% == M goto Cytron
set/p _ans3 = Are you using a Keyboard FeatherWing (Y/N)?:
if %_ans3% == N goto bbkeyboard
if %_ans3% == n goto bbkeyboard
if %_ans3% == Y goto kbdFeatherW
if %_ans3% == y goto kbdFeatherW
echo Invalid Selection (Y or N)
goto skip_codecopy

:kbdFeatherW
copy /cpython/kbdFeatherWing/* /
if not exist /lib mkdir /lib
copy /cpython/kbdFeatherWing/lib/* /lib/
rename /lib/pydos_ui.py /lib/pydos_ui_uart.py
echo copy /lib/pydos_ui_kfw.py /lib/pydos_ui.py
copy /lib/pydos_ui_kfw.py /lib/pydos_ui.py
if %_ans2% == O del /lib/kfw_s2_board.py
if %_ans2% == E del /lib/kfw_pico_board.py
goto wifienv

:bbkeyboard
set/p _ans3 = Do you have a BB Q10/Q20 I2C keyboard connected (Y/N)?:
if %_ans3% == N goto Cytron
if %_ans3% == n goto Cytron
if %_ans3% == Y goto keyboardui
if %_ans3% == y goto keyboardui
echo Invalid Selection (Y or N)
goto bbkeyboard

:keyboardui
rename /lib/pydos_ui.py /lib/pydos_ui_uart.py
echo copy /cpython/lib/optional/pydos_ui_bbkeybd.py /lib/pydos_ui.py
copy /cpython/lib/optional/pydos_ui_bbkeybd.py /lib/pydos_ui.py
rem Make kfw copy so that ui.bat can be used to switch modes
copy /cpython/lib/optional/pydos_ui_bbkeybd.py /lib/pydos_ui_kfw.py
copy /cpython/kbdFeatherWing/*.bat /
copy /cpython/kbdFeatherWing/lib/bbq10keyboard.* /lib/

:Cytron
if not %_ans2% == O goto wifienv
set/p _ans3 = Are you using a Cytron Maker Pi Pico (Y/N)?:
if %_ans3% == N goto wifienv
if %_ans3% == n goto wifienv
if %_ans3% == Y goto MakerPiPico
if %_ans3% == y goto MakerPiPico
echo Invalid Selection (Y or N)
goto Cytron

:MakerPiPico
if %_ans% == C goto CPCytron
echo copy "/mpython/boardconfigs/pydos_bcfg_Cytron Maker Pi Pico.py" /lib/pydos_bcfg.py
copy/y "/mpython/boardconfigs/pydos_bcfg_Cytron Maker Pi Pico.py" /lib/pydos_bcfg.py
goto wifienv

:CPCytron
if not exist /lib mkdir /lib
copy/y /cpython/CytronMPP/lib/* /lib/
echo copy /cpython/boardconfigs/pydos_bcfg_cytron_maker_pi_pico.py /lib/pydos_bcfg.py
copy/y /cpython/boardconfigs/pydos_bcfg_cytron_maker_pi_pico.py /lib/pydos_bcfg.py

:wifienv
if "%_boardID%" == "matrixportal_m4" goto entercreds
if %_ans2% == O goto done

:entercreds
set/p _ans3 = Enter Wifi credentials now (/settings.toml file can be edited later) (Y/N)?:
if %_ans3% == N goto done
if %_ans3% == n goto done
if %_ans3% == Y goto dotenv
if %_ans3% == y goto dotenv
echo Invalid Selection (Y or N)
goto entercreds

:dotenv
setenv.py
ntpdate.py -4

:done
set _ans=
set _ans2=
set _ans3=
reboot
