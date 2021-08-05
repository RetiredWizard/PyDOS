@echo off
set/p branch=Enter branch number:
goto lab%branch%
echo bad selection
goto done
:lab1
echo one
goto done
:lab2
echo two
goto done
:lab3
echo three
goto done
:done
exit %branch%
