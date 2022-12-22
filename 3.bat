@echo off
if exist autoexec.bat copy/y autoexec.bat _PyDexec._PyD
copy/y 3.aut autoexec.bat
runvm /PyBasic/PyBasic adventure-fast.pgm
menu.bat