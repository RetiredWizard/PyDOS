@echo off
if exist _autoexec._PyD goto skip
if exist autoexec.bat rename autoexec.bat _autoexec._PyD
:skip
copy/y 3.aut autoexec.bat
runvm /PyBasic/PyBasic adventure-fast.pgm
menu.bat