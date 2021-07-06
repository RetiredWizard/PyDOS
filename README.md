Micropython DOS-like OS for RP2040 microcontroller boards. Check out the demo video at https://www.youtube.com/watch?v=Az_oiq8GE4Y

To start the OS type "import PyDOS" at the micropython REPL prompt.

External programs included:

edit.py - line editor inspired by DOS edlin. Intial program structure of line editor by Joesph Long
    https://github.com/j-osephlong/Python-Text-Editor

fileview.py - scrollable text file viewer

sdmount.py - mounts an sd card to the file system

sdumount.py - dismounts an sd card from the file system

setdate.py - initalizes the RP2040 real time clock to an entered date

settime.py - initalizes the RP2040 real time clock to an entered time

diff.py - performs a file comparison

sound.py - outputs a sound to a speaker cicruit connected to GPIO 20

lcdprint.py - displays text on an I2C LCD display

PyBasic.py - a Basic interpreter from https://github.com/richpl/PyBasic. Tweaked and modified to run on Micropython.
	basicparser.py, basictoken.py, flowsignal.py, lexer.py, program.py

At the DOS prompt a python program can be run by simply entering the filename (with or without the .py extension)
