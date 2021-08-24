@echo off
:tryagain
set/p _ans = (C)ircuit Python or (M)icropython: 
if %_ans% == c goto cpython
if %_ans% == C goto cpython
if %_ans% == m goto mpython
if %_ans% == M goto mpython
echo Invalid selection (C or M)
goto tryagain
:cpython
set _ans = C
copy /cpython/* /
goto board
:mpython
set _ans=M
copy /mpython/* /
:board
set/p _ans2 = (T)hingPlus, (F)eather, (N)anoConnect, (O)ther:
if %_ans2% == t goto thingplus
if %_ans2% == T goto thingplus
if %_ans2% == f goto feather
if %_ans2% == F goto feather
if %_ans2% == n goto nanoconnect
if %_ans2% == N goto nanoconnect
if %_ans2% == o goto other
if %_ans2% == O goto other
echo Invalid selection (T,F,N or O)
goto board
:thingplus
if %_ans% == C goto other
copy /mpython/ThingPlus/* /
goto other
:feather
if %_ans% == M goto other
copy /cpython/Feather/* /
if not exist /lib mkdir /lib
copy /cpython/Feather/lib/* /lib/
if not exist /lib/adafruit_character_lcd mkdir /lib/adafruit_character_lcd_mkdir
copy /cpython/Feather/lib/adafruit_character_lcd/* /lib/adafruit_character_lcd/
if not exist /lib/adafruit_mcp230xx mkdir /lib/adafruit_mcp230xx
copy /cpython/Feather/lib/adafruit_mcp230xx/* /lib/adafruit_mcp230xx/
goto other
:nanoconnect
if %_ans% == M goto other
copy /cpython/NanoConnect/* /
goto other
:other
set _ans=
set _ans2=
