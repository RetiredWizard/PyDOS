## PyDOS, PyBASIC, edit... All the functionality of the 1981 IBM PC on a PI Pico?

**MicroPython/CircuitPython DOS-like shell for microcontroller boards**   
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
(if you're not using MicroPython) folder from the downloaded repository files. Within the remaining Python folder (**cpython** or **mpython**) are folders
for specific micro controller boards,
you can free up further space by deleting anything other than the board you are using. Finally, after running the **setup.bat** file in PyDOS you can
delete both the **cpython** and **mpython** folders as they are only used by the **setup.bat** script.

**CircuitPython Setup**

For CircuitPython the first thing you should do is compile a custom CircuitPython image. (see https://www.youtube.com/watch?v=sWy5_B3LL8c for a demonstration)
Upon downloading the latest version of CircuitPython from the
github repository, modify the **py/circuitpy_mpconfig.h** file and change the value on the line that reads "**#define MICROPY_ENABLE_PYSTACK**" from "(1)" to "(0)". Once
that is done you can follow the setps in https://learn.adafruit.com/building-circuitpython/build-circuitpython and demonstrated in the YouTube video mentioned above.

+An addtional compiler option is required when running PyDOS on an ESP32S2 microcontroller. Modify the **py/mpconfig.h** file and change the value on the line that reades 
"**#define MICROPY_STACKLESS"** from "(0)" to "(1)".

**PyDOS will run without using this custom CircuitPython image however PyBasic and some of the other applications will not run as well since PyDOS will be memory limited.**

To install the custom CircuitPython image, put your microcontroller board in "bootloader" mode and copy the compiled .UF2 file to the USB mass storage device that
shows up on your host computer.

After the .UF2 file is copied to the microcontroller board it should re-boot and a new USB mass storage device should appear. 

To copy PyDOS to the Microcontroller, simply drag the PyDOS directory structure
(after removing the **mpython** folder if space is a concern) to the root directory of the device that appears on the host computer.
Your microcontroller now has PyDOS installed.

At this point the microcontroller file system is set to allow computer Read/Write access, however the boot.py file that you copied
with PyDOS will switch the mode so that
PyDOS has Read/Write access and the host computer will only have ReadOnly access. This change won't take effect until you power cycle the micro controller board so **be
sure that the PyDOS files are all copied before turning the power off on your microcontroller board**. If the copy is interrupted for any reason (it's possible that the
CircuitPython auto-reload feature may interrupt the copy) you can delete the boot.py file in the root of the microcontroller flash, to be sure the file system doesn't
switch modes and try the copy again. If you do find your self locked out of the flash from the host computer and PyDOS is not running, you can recover using one
of the following options.

+ Ground Pin D5 and power cycle the microcontroller board
+ If the **fs.py** file was copied to the cpython folder you can launch it from the REPL as follow:

	    import os
	    os.chdir("/cpython")
	    import fs
	    This program will set the CircuitPython filesystem access mode AFTER the next
	    Powercycle. A Control-D will NOT reset the filesystem access mode.
	    
	    Enter RO or RW: RO                 # Entering an RO here will all the Host compter to have Read Write access

+ If the **edit.py** file was copied you can launch edit from the REPL by typing "import edit". You can then use edit to modify line 16 of boot.py as follows:

	   import edit
	   h for command list
	   : o boot.py
	   boot.py: 15L
	      * 15 PyDOSReadOnly = False    # If this line isn't displayed you may need to enter the L command to locate it
	   boot.py: 15R"False","True"
	   boot.py: e

* If the **boot.ro** file was copied to the cpython folder you can copy it to /boot.py from the repl as follows:

	    file1 = open("/cpython/boot.ro")
	    file2 = open("/boot.py","w")
	    file2.write(file1.read())
	    
+ If none of these options work, you may need to erase everything on the flash and start the PyDOS copy again:

	    import storage
	    storage.erase_filesystem()


At this point, if the copy worked without any errors, you should power cycle the microcontroller board so that the file system is configured to allow
the microcontroller to have Read/Write access.

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
