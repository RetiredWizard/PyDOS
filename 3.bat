@echo off
if not exist /runvm.py goto micropython
if exist autoexec.bat copy autoexec.bat autoexec.sav
copy/y 3.aut autoexec.bat
runvm "PyBasic/PyBasic adventure-fast.pgm"
:micropython
cd /PyBasic
pexec import PyBasic
pexec PyBasic.main("adventure-fast.pgm")
cd /
menu.bat