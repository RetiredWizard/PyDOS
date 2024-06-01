@echo off
pexec import board
pexec envVars["_boardID"] = board.board_id
if not "%_boardID%" == "lilygo_tdeck" goto kbdFeatherWing
echo .
echo     Entered Lilygo Keys    Results
echo     -------------------    -------
echo              _-               =
echo              (+               [
echo              +)               ]
echo              (-               <
echo              -)               >
echo              _#               ^
echo              _/               \
echo              -/               %%
echo Speaker Key (left of enter)   $
echo Track ball up                 up arrow
echo Track ball down               down arrow
echo Track ball left               left arrow
echo Track ball right              right arrow
echo .
goto done

:kbdFeatherWing
echo Alt-$ (Speaker) returns an equal sign (=)
echo Hold a key for 2 seconds SHIFT or ALT
echo Alt-Enter will toggle between SHIFT and ALT
echo Alt-Space will enable SHIFT Lock or ALT Lock
echo Shift when SHIFT Lock returns lower case
echo The Microphone symbol returns a left bracket ([)
echo 2 second Shift on Microphone = right bracket (])
echo Shift Lock Microphone Symbol = right bracket (])
echo 2 second Shift on dollar sign ($) = percent (%%)
echo Shift Lock dollar sign ($) = percent (%%)
echo joystick up/down scrolls through entered lines
echo The F3 key retrieves the last entered line
echo F2 and then pressing a key will search
echo    the last entered line for that character

:done
pause
