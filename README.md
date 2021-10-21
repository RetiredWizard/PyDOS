## PyDOS, PyBASIC, edit... All the functionality of the 1981 IBM PC on a PI Pico?


**MicroPython DOS-like shell for microcontroller boards**   
**Check out the demo video at https://www.youtube.com/watch?v=Az_oiq8GE4Y**

To start the shell type **import PyDOS** at the micropython REPL prompt.

**setup.bat** in the root folder will prompt the user to indicate Circuit Python or Micropython and then the board they are using.
The setup batch file will then copy the programs and libraries appropriate for the user's platform to the root folder of the
Microcontroller flash.

External programs included:

**runasthread.py** (Micropython only) - This program will attempt to launch a python program on the second RP2040 core. Threading is
experimental on Micropython so it's not difficult to crash the microcontroller using this program. I have not found a way to kill
a thread started on the second core so be sure any threads you launch will shutdown on their own or monitor a global variable or
thread.lock to respond to a shutdown request (see the badblink.py for an example).

**edit.py** - line editor inspired by DOS edlin. Intial program structure of line editor by Joesph Long
    https://github.com/j-osephlong/Python-Text-Editor
    
**fsedit.py** - shell to load full screen editor from https://github.com/robert-hh/Micropython-Editor

**fileview.py** - scrollable text file viewer

**sdmount.py** (Micropython only) - mounts an sd card to the file system

**sdumount.py** (Micropython only) - dismounts an sd card from the file system

**setdate.py** (Micropython only) - initalizes the RP2040 real time clock to an entered date

**settime.py** (Micropython only) - initalizes the RP2040 real time clock to an entered time

**diff.py** - performs a file comparison

**sound.py** - outputs a sound to a speaker cicruit connected to GPIO 19

**lcdprint.py** - displays text on an I2C LCD display

**PyBasic.py** - a Basic interpreter from https://github.com/richpl/PyBasic. Tweaked and modified to run on Micropython.
	basicparser.py, basictoken.py, flowsignal.py, lexer.py, program.py, basicdata.py

At the DOS prompt a python program (.py) or batch (.bat) file can be run by simply entering the filename with or without
the extension

## Installation

If the board you're using has limited flash storage you can delete either the **cpython** (if you're not using CircuitPython) or **mpython**
(if you're not using Micro Python) folder from the downloaded repository files. Within the remaining Python folder (**cpython** or **mpython**) are folders
for specific micro controller boards,
you can free up further space by deleting anything other than the board you are using. Finally, after running the **setup.bat** file in PyDOS you can
delete both the **cpython** and **mpython** folders as they are only used by the **setup.bat** script.

**CircuitPython Setup**

For CircuitPython the first thing you should do is compile a custom CircuitPython image. (see https://www.youtube.com/watch?v=sWy5_B3LL8c for a demonstration)
Upon downloading the latest version of CircuitPython from the
github repository, modify the **py/circuitpy_mpconfig.h** file and change the value on the line that reads "**#define MICROPY_ENABLE_PYSTACK**" from "(1)" to "(0)". Once
that is done you can follow the setps in https://learn.adafruit.com/building-circuitpython/build-circuitpython and demonstrated in the YouTube video mentioned above.

To install the custom CircuitPython image, put your microcontroller board in "bootloader" mode and copy the compiled .UF2 file to the USB mass storage device that
shows up on your host computer.

After the .UF2 file is copied to the microcontroller board it should re-boot and a new USB mass storage device should appear. Simply drag the PyDOS directory structure
(after removing the **mpython** folder if space is a concern) to the root directory of the device that appears. Your microcontroller now has PyDOS installed.

At this point you should power cycle the microcontroller board so that the file system is configured to allow the microcontroller to have Read/Write access.

To interact with the microcontroller you will need to connect using a terminal program. On a PC you can use putty and on linux minicom works well. To start minicom
on linux type the command:

          Term=linux minicom -b 115200 -o -D /dev/ttyACM0
	  
You should be presented with the REPL prompt (>>>), if not, press return or Ctrl-C.

At the REPL prompt type "**import PyDOS*** to start PyDOS and then type **setup** to run the customization script.

**MicroPython Setup**

You can use a standard MicroPython image downloaded from Micropython.org to run PyDOS. Once your microcontroller has Micropython installed and running the best way
to copy the PyDOS files and interact with the repl is to use MPRemote. Detailed documentation on installing and using MPRemote can be found 
at https://docs.micropython.org/en/latest/reference/mpremote.html.

To install PyDOS on the microcontroller board download PyDOS from github repository and after deleting the **cpython** folder if space is an issue, set your current
directory to the root folder of the downloaded PyDOS repository and use the following command:

	mpremote fs cp -r * :
	
To interact with the microcontroller you can connect to the REPL by simply typing **mpremote** and pressing return several times until the REPL prompt
(>>>) is displayed.

At the REPL prompt type "**import PyDOS*** to start PyDOS and then type **setup** to run the customization script.
