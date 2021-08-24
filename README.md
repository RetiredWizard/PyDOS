Micropython DOS-like shell for RP2040 microcontroller boards. Check out the demo video at https://www.youtube.com/watch?v=Az_oiq8GE4Y

To start the shell type "import PyDOS" at the micropython REPL prompt.

setup.bat in the root folder will prompt the user to indicate Circuit Python or Micropython and then the board they are using.
The setup batch file will then copy the programs and libraries appropriate for the user's platform to the root folder of the
Microcontroller flash.

External programs included:

runasthread.py (Micropython only) - This program will attempt to launch a python program on the second RP2040 core. Threading is
experimental on Micropython so it's not difficult to crash the microcontroller using this program. I have not found a way to kill
a thread started on the second core so be sure any threads you launch will shutdown on their own or monitor a global variable or
thread.lock to respond to a shutdown request (see the badblink.py for an example).

edit.py - line editor inspired by DOS edlin. Intial program structure of line editor by Joesph Long
    https://github.com/j-osephlong/Python-Text-Editor

fileview.py (Micropython only) - scrollable text file viewer

sdmount.py (Micropython only) - mounts an sd card to the file system

sdumount.py (Micropython only) - dismounts an sd card from the file system

setdate.py (Micropython only) - initalizes the RP2040 real time clock to an entered date

settime.py (Micropython only) - initalizes the RP2040 real time clock to an entered time

diff.py - performs a file comparison

sound.py - outputs a sound to a speaker cicruit connected to GPIO 20

lcdprint.py - displays text on an I2C LCD display

PyBasic.py - a Basic interpreter from https://github.com/richpl/PyBasic. Tweaked and modified to run on Micropython.
	basicparser.py, basictoken.py, flowsignal.py, lexer.py, program.py, basicdata.py

At the DOS prompt a python program (.py) or batch (.bat) file can be run by simply entering the filename with or without
the extension
