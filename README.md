## PyDOS, PyBASIC, edit... All the functionality of the 1981 IBM PC on a PI Pico?

**MicroPython/CircuitPython DOS-like shell for microcontroller boards:**  
**(RP2040, ESP32, ESP32 PICO-D4, ESP32-S2/S3, nRF52840, SAMD51, stm32L4+, NXM ARM Cortex-M7)**  

**Check out the demo video at https://www.youtube.com/watch?v=Az_oiq8GE4Y**

To start the shell type **import PyDOS** at the micropython REPL prompt.

At the PyDOS prompt a python program (.py) or batch (.bat) file can be run by simply entering the filename with or without
the extension.

**setup.bat** in the root folder, will prompt the user to indicate the board they are using.
The setup batch file will then copy the programs and libraries appropriate for the user's
 platform to the root and /lib folders of the Microcontroller flash.

## Implemented DOS Commands:  
(syntax and descriptions taken from https://home.csulb.edu/~murdock/dosindex.html)

PyDOS requires all switches to immediatly following the command with no spaces between the command or switches.

If a command argument contains spaces the argument must be enclosed in quotes.

**REM [comment]** - Used in batch files to insert remarks (that will not be acted on).

**DIR[/P][/W] [path][filename]** - Displays directory of files and directories stored on flash.

**DATE** - Displays the current date.

**TIME** - Displays the current time.

**MEM[/D]** - Displays available RAM and performs a garbage collection operation

**VER** - Displays PyDOS version

**ECHO [ON|OFF][message]** - Displays messages or turns on or off the display of commands in a batch file.

**PAUSE** - Suspends execution until a key is pressed.

**GOTO label** Causes unconditional branch to the specified label. (labels are defined as :label in batch files)

**IF [NOT] EXIST filename (command) [parameters]**  
**IF [NOT] (string1)==(string2) (command) [parameters]** - Allows for conditional operations in batch processing.  
**IF [NOT] ERRORLEVEL (number) (command) [parameters]**  

**SET[/P] (string1)=[(string2|prompt)]** - Inserts strings into the command environment. The set values can be used later by programs.

**PROMPT [prompt text]** = Changes the DOS command prompt. Supported strings "$R,$D,$T,$P,$G,$C,$F,$A,$B,$E,$H,$L,$Q,$S,$V,$_,$."

**RENAME (REN, MOVE, MV) [path]filename [path]filename** - Changes the filename under which a file is stored.

**DELETE (DEL) [path]filename** = Deletes files from disk.

**TYPE (MORE)[/P] [path]filename** - Displays the contents of a file.

**CD [[d:]path]** - Displays working (current) directory and/or changes to a different directory.  
**CD ..** - Changes to parent directory of current directory.

**MKDIR (MD) path** - Creates a new subdirectory.

**RMDIR (RD) path** - Removes a subdirectory.

**COPY[/Y] [path]filename [path][filename]** - copies files.

**EXIT** - In a batch file returns to PyDOS, at PyDOS prompt terminates PyDOS and returns to REPL.

**PEXEC [python command]** - Executes a single python command.

An **autoexec.bat** batch file will automatically execute when PyDOS starts.

### External programs included:

**pydospins.py** - Displays the GPIO pins for sound output and I2C for the particular board PyDOS is running on.

**PyBasic.py** - a Basic interpreter from https://github.com/richpl/PyBasic. Tweaked and modified to run on Micropython and Circuitpython.
	basicparser.py, basictoken.py, flowsignal.py, lexer.py, program.py, basicdata.py
	
**runasthread.py** (Micropython only) - This program will attempt to launch a python program on the second RP2040 core. Threading is
experimental on Micropython so it's not difficult to crash the microcontroller using this program. I have not found a way to kill
a thread started on the second core so be sure any threads you launch will shutdown on their own or monitor a global variable or
thread.lock to respond to a shutdown request (see the badblink.py for an example).

**runvm.py** (Circuitpython only) - This program will use the **supervisor.set_next_code_file** method to configure the microcontroller
board to launch the specfied python script after the next soft reboot. The program then uses the **supervisor.reload()** method to 
perform a reboot and launch the target script. The target script is "wrapped" in some code that passes any specified arguments and the
PyDOS environment variables to the newly booted environment as well as code that causes a second soft reboot after the script has completed
to return control to PyDOS.

**edlin.py** - line editor inspired by DOS edlin. Intial program structure of line editor by Joesph Long
    https://github.com/j-osephlong/Python-Text-Editor
    
**edit.py** - shell to load full screen editor from https://github.com/robert-hh/Micropython-Editor

**fileview.py** - scrollable text file viewer

**sdmount.py** - mounts an sd card to the file system
**sdumount.py** - dismounts an sd card from the file system

**setdate.py** - initalizes the real time clock to an entered date  
**settime.py** - initalizes the real time clock to an entered time  
**ntpdate.py** (ESP32xxx and Pico W only) - sets the time and date using the Internet NTP protocol

**diff.py** - performs a file comparison

**sound.py** - outputs a sound to a speaker cicruit connected to GPIO pin defined in lib/pydos_bcfg.py  
**tsound.py** - test program that plays a short sound sequence  
**piano.py** - emulates a small piano keyboard

**i2cscan.py** - scans the I2C bus and displays any found device addresses

**lcdprint.py** - displays text on an I2C LCD display  
**lcdscroll.py** - scrolls text on an I2C LCD display  
**temperature.py** - displays temperature value from onboard temperature sensor to screen and I2C LCD display

**basicpython.py** - Shell modeled after basic interpreter shell from https://github.com/tannewt/basicpython

**blink.py** - program to blink onboard LED

**rgbset.py** - program to set the rgb color of an onboard neopixel or dotstar  
**rgbblink.py** - program to blink an onboard neopixel or dotstar  
**rgbrainbow.py** - program to color cycle an onboard neopixel or dotstar  

**reboot.py** - performs a soft reboot (Micropython requires a Ctrl-D to complete)

**keys.bat** - (Keyboard Featherwing only) Displays keyboard mappings for hidden keys and functions  
**ui.bat** - (Keyboard Featherwing only) Switches between using the Keyboard Featherwing and USB Serial port for PyDOS I/O

**fs.py** - (Circuitpython only) By selecting the "RO" option the flash mode is set such that when the microcontroller
is power cycled or hard reset, the host computer will have read/write access to the flash and the microcontoller will be
restricted to read only access. To give PyDOS access to the flash after switching to this mode the boot.py file must be
replaced or modified from the host computer so that it contains the following instructions:

    import storage
    storage.remount("/",False)
    
and then power cycled or hard reset.


## Installation

If the board you're using has limited flash storage you can delete either the **cpython** (if you're not using CircuitPython) or **mpython**
(if you're not using MicroPython) folder from the downloaded repository files. Within the remaining Python folder (**cpython** or **mpython**) are folders
for specific micro controller boards, you can free up further space by deleting anything other than the board you are using (the "Pico W" board uses the ESP folder). Finally, after running
the **setup.bat** file in PyDOS you can delete both the **cpython** and **mpython** folders as they are only used by the **setup.bat**
script. For very limited Flash boards you may want to delete the **PyBasic** folder until after setup is run. Once setup has ben run, delete the **cpython/mpython** folders from
the microcontroller and copy as much of the **PyBasic** directory as space permits, copying just the *.py files is all that's needed for PyBasic to run.

**Building custom CircuitPython firmware**

For CircuitPython the first thing you should do is compile a custom CircuitPython image, the steps for doing so are described in the Adafruit learning guide
at: https://learn.adafruit.com/building-circuitpython/build-circuitpython.  Upon downloading the latest version of CircuitPython from the github repository,
modify the **py/circuitpy_mpconfig.h** file and change the value on the line that reads "#**define MICROPY_ENABLE_PYSTACK**" from "(1)" to "(0)". On an 
ESP32S2 microcontroller it's also necessary to modify the **py/mpconfig.h** file and change the value on the line that reades "**#define MICROPY_STACKLESS**"
from "(0)" to "(1)". You can find custom UF2 images for some boards as release resources here: https://github.com/RetiredWizard/PyDOS/releases. If you're using a board not included you
can open a Github issue on this repository to request it.

An earlier version of the build process is demonstrated in the YouTube video at: https://www.youtube.com/watch?v=sWy5_B3LL8c, but be sure to check the Adafruit
guide and use the updated instructions.

**PyDOS will run without using this custom CircuitPython image however PyBasic and some of the other applications will not run as well since PyDOS will be memory limited.**

**CircuitPython Setup**

To install the custom CircuitPython image, put your microcontroller board in "bootloader" mode and copy the compiled .UF2 file to the USB mass storage device that
shows up on your host computer.

After the .UF2 file is copied to the microcontroller board it should re-boot and a new USB mass storage device should appear. 

To copy PyDOS to the Microcontroller, simply drag the PyDOS directory structure
(after removing the **mpython** folder if space is a concern) to the root directory of the device that appears on the host computer.
Your microcontroller now has PyDOS installed.

If the copy worked without any errors, you should power cycle the microcontroller board so that the file system is configured to allow
the microcontroller to have Read/Write access.

**PyDOS has Read/Write access and the host computer will only have ReadOnly access. This change won't take effect until you have completed the power cycle mentioned above, so be
sure that the PyDOS files are all copied before turning the power off on your microcontroller board. If the copy is interrupted for any reason you can delete the boot.py
file in the root of the microcontroller flash and try the copy again. 

If you find yourself locked out of the flash from the host computer and PyDOS is not running, the easiest way to recover is to
connect to the REPL, remove the boot.py file and then power cycle the microcontroller board. 

        import os
        os.remove("boot.py")
**
To interact with the microcontroller you will need to connect using a terminal program. On a PC you can use putty and on linux minicom works well. To start minicom
on linux type the command:

          Term=linux minicom -b 115200 -o -D /dev/ttyACM0
	  
You should be presented with the REPL prompt (>>>), if not, press return or Ctrl-C.

At the REPL prompt type "**import PyDOS**" to start PyDOS and then type **setup** to run the customization script.

--------------------------------------------------------------------------------------------------------------------
**Building custom Micropython firmware**

Although you can use a standard Micropython image downloaded from Micropython.org to run PyDOS, there are two reasons you may want to build a custom
Micropython firmware file. 

The first is if you wan to connect up an old school serial terminal to the REPL rather than the standard serial over USB connection. Instructions for building 
Micropython with this modification can be found in section 2.2 of the Raspberry Pi Pico Python SDK at https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf.

The second is that PyDOS uses a recursive routine to process wildcard operations and the default stack in Micropython limits the recursion depth that can be obtained (**With more recent versions of Micropython this has become much less of an issue).
This means that PyDOS has to limit wildcard operations, one impact of this is that files with longer file names may not appear
in directory listings when wildcards are used. To eliminate this issue a custom Micropython image can be built with the the MICROPY_STACKLESS parameter in **py/circuitpy_mpconfig.h**
changed from **0** to **1**. 

**MicroPython Setup**

Once your microcontroller has Micropython installed and running the best way
to copy the PyDOS files and interact with the repl is to use Thonny. Adafruit has a good learning guide for getting started with Thonny here:
https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/micropython-installation. 

Download PyDOS from the github repository and after deleting the **cpython** folder if space is an issue, use the Thonny upload command as described in the Adafruit 
learning guide to copy the downloaded files to the microcontroller.

To interact with the microcontroller connect over the serial USB port (COMn: /dev/ttyACMx, etc) using a terminal program like puTTY or minicom. You can use the Thonny shell as well
however, it does not support the basic ansi escape sequences used by some of the PyDOS functions.
One thing to note is that if you
connect to your microcontroller with a terminal program after using Thonny, you may need to press CTRL-B to exit the raw REPL mode that 
Thonny uses to transfer and execute files.

Another option is to use MPRemote. Detailed documentation on installing and using MPRemote can be found 
at https://docs.micropython.org/en/latest/reference/mpremote.html.

To install PyDOS on the microcontroller board download PyDOS from the github repository and after deleting the **cpython** folder if space is an issue, set your current
directory to the root folder of the downloaded PyDOS repository and use the following command:

	mpremote fs cp -r * :
	
To interact with the microcontroller you can connect to the REPL by simply typing **mpremote** and pressing return several times until the REPL prompt
(>>>) is displayed.

At the REPL prompt type "**import PyDOS*** to start PyDOS and then type **setup** to run the customization script.
