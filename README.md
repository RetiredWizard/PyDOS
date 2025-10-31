## PyDOS, PyBASIC, edit... All the functionality of the 1981 IBM PC on a PI Pico?

**MicroPython/CircuitPython DOS-like shell for microcontroller boards:**  
**(RP2040, RP2350, ESP32, ESP32 PICO-D4, ESP32-S2/S3, nRF52840, SAMD51, stm32L4+, NXM ARM Cortex-M7, Lilygo T-Deck, M5Stack Cardputer, Cheap Yellow Display - esp32-2432s028)**  

**Check out the demo video at https://www.youtube.com/watch?v=Az_oiq8GE4Y**

*Related Repositories:*  
[PyDOS_virtkey](https://github.com/RetiredWizard/PyDOS_virtkeyboard) - The modules needed to add virtual keyboard support to PyDOS  
[PyDOS_wifi](https://github.com/RetiredWizard/PyDOS_wifi) - Generalized Python based microcontroller WiFi API

See the Installation section below to install all the external commands and customize the install for the particular microcontroller you are using. However, **if you just want to launch the shell or have limited flash space, the PyDOS.py program will run standadlone** so you can simply copy **PyDOS.py** to your microcontroller to begin.

To start the shell type **import PyDOS** at the REPL prompt.

At the PyDOS prompt a python program (.py) or batch (.bat) file can be run by simply entering the filename with or without
the extension.

**setup.bat** in the root folder, will prompt the user to indicate the the type of board they are using.
The setup batch file will then copy the programs and libraries appropriate for the user's
 platform to the root and /lib folders of the Microcontroller flash.

## Implemented DOS Commands:  
(syntax and descriptions taken from https://home.csulb.edu/~murdock/dosindex.html)

When run on an operating system that uses a forward slash as the Directory Seperator, PyDOS requires all switches to immediatly follow the command with no spaces between the command or switches. This 
is necessary becuase the forward slash directory seperator conflicts with the DOS switch seperator. If the PyDOS environement variable DIRSEP is set to \ (i.e. `set DIRSEP=\`) PyDOS will utilize the traditional backslash as the directory seperator and DOS switches can then be placed anywhere on the command line.
Many of the messages displayed by PyDOS and virtually all external Python programs will not respect this environment variable so the *nix forward slash seperator may still be displayed or required when inputting path names to external programs.

If a command argument contains spaces the argument must be enclosed in quotes.

**REM [comment]** - Used in batch files to insert remarks (that will not be acted on).

**DIR[/P][/W][/S] [path][filename]** - Displays directory of files and directories stored on flash.
- /P Pauses after each screenful of information (Q or C to abort listing)  
- /W Uses wide list format, displaying file/folder names only  
- /S Displays files recursively, traversing any subdirectories  

**DATE** - Displays the current date.

**TIME** - Displays the current time.

**MEM[/D]** - Displays available RAM and performs a garbage collection operation  
- /D Include debug information when supported by microcontroller board

**VER** - Displays PyDOS version

**ECHO [ON|OFF][message]** - Displays messages or turns on or off the display of commands in a batch file.

**PAUSE** - Suspends execution until a key is pressed.

**GOTO label** Causes unconditional branch to the specified label. (labels are defined as :label in batch files)

**IF [NOT] EXIST filename (command) [parameters]**  
**IF [NOT] (string1)==(string2) (command) [parameters]** - Allows for conditional operations in batch processing.  
**IF [NOT] ERRORLEVEL (number) (command) [parameters]**  

**SET[/P][/A] (variable)=[(string|prompt)]** - Inserts strings into the command environment. The set values can be used later by programs.  
- /A specifies that the string to the right of the equal sign is a numerical expression that is evaluated  
- /P displays the specified prompt string before setting the value of a variable to a line of input entered by the user  
*DOS specific environment variables:*
    - LIB - The Python search path for importing libraries (the current directory is always searched first but not included in the LIB variable)  
    - PATH - The directory search list for executing python scripts and DOS batch files (the current directory is always searched first but not included in the PATH variable)
    - PROMPT - The DOS prompt string
    - _scrHeight - The number of lines on the terminal or screen
    - _scrWidth - The number of columns on the terminal or screen
    - _displayTerm - After running a python program PyDOS will make sure the terminal is restored to an attached displayio display unless _displayTerm is set to "N".  
    - errorlevel - The result code from the previous BAT file or pexec command executed
    - DIRSEP - If set to a backslash (\\) PyDOS will use a backslash as the directory seperator character regardless of the seperator used by the local filesystem (i.e. `os.sep`). If set to anything other than a backslash PyDOS will use a forward slash as the directory seperator character.

**PROMPT [prompt text]** - Changes or displays the DOS command prompt. Supported strings "$R,$D,$T,$P,$G,$L,$C,$F,$A,$B,$E,$H,$Q,$S,$V,$_,$$" and text literals  
Example: `prompt $e[44m$p$g` sets the backgound blue (if the terminal supports vt100 escape sequences) and displays the current directory followed by a ">"

```
Character	Description
---------   -----------
$R          Available RAM
$D          Current date
$T          Current time
$P          Current path
$G          > (Greater than sign)
$L          < (Less than sign)
$C          ( (Left parenthesis)
$F          ) (Right parenthesis)
$A          & (Ampersand)
$B          | (Pipe symbol)
$E          ANSI escape code (code 27)
$H          Backspace (delete last character from displayed prompt)
$Q          = (Equal sign)
$S          Space
$V          Version number
$_          ENTER-LINEFEED
$$          $ (Dollar sign)
```

**PATH [path1;path2;...]** - Changes or displays the directory search list for executing python scripts and DOS batch files

**RENAME (REN, MOVE, MV) [path]filename [path]filename** - Changes the filename under which a file is stored.

**DELETE (DEL)[/S] [path]filename** - Deletes files from disk.  
- /S Delete specified files from all subdirectories

**TYPE (MORE)[/P] [path]filename** - Displays the contents of a file.  
- /P Pauses after each screenful of information (Q or C to abort listing)

**CD [[d:]path]** - Displays working (current) directory or changes to a different directory.  
**CD ..** - Changes to parent directory of current directory.

**MKDIR (MD) path** - Creates a new subdirectory.

**RMDIR (RD)[/S] path** - Removes a subdirectory.  
- /S Removes all directories and files in the specified directory and the directory itself

**COPY[/Y] [path]filename [path][filename]** - copies files.  
- /Y Suppresses prompting to confirm you want to overwrite an existing destination file

**EXIT** - In a batch file returns to PyDOS, at PyDOS prompt terminates PyDOS and returns to REPL.

**PEXEC[/Q] [python command]** - Executes a single python command.
- /Q Supresses error message if error condition occurs (errorlevel variable is set)

An **autoexec.bat** batch file will automatically execute when PyDOS starts.

### External programs included:
*External programs may require one-time board configuration using setup.bat*

**pydospins.py** - Displays the GPIO pins for sound output and I2C for the particular board PyDOS is running on.

**PyBasic.py [[path]basic program file .py|.bas]** - a Basic interpreter from https://github.com/richpl/PyBasic. Tweaked and modified to run on Micropython and Circuitpython.
	interpreter.py, basicparser.py, basictoken.py, flowsignal.py, lexer.py, program.py, basicdata.py
	
**runasthread.py [[path]python program file[.py]]** (Micropython only) - This program will attempt to launch a python program on the second RP2040 core. Threading is
experimental on Micropython so it's not difficult to crash the microcontroller using this program. I have not found a way to kill
a thread started on the second core so be sure any threads you launch will shutdown on their own or monitor a global variable or
thread.lock to respond to a shutdown request (see the badblink.py for an example).

**runvm.py [[path]python program file[.py]]** - This program is used to launch Python programs that require more memory
than is available while running PyDOS. **runvm** will write a **code.py**/**main.py**
file which launches the specfied python program after the next soft reboot. The program then
uses **supervisor.reload()** for CircuitPython or **sys.exit** for MicroPython to
perform a reboot (sys.exit requires a Ctrl-D to complete the operation). The specified python
program is "wrapped" in some code that passes any command line arguments and the PyDOS
environment variables to the newly booted environment as well as code that restores the
original **code.py**/**main.py** files and causes a second soft reboot returning control to
PyDOS.

**virtrepl.py** - Launches a python REPL that can be run from PyDOS. Type "exit" to close and return to PyDOS.

**edlin.py [[path]filename]** - line editor inspired by DOS edlin. Intial program structure of line editor by Joesph Long
    https://github.com/j-osephlong/Python-Text-Editor
    
**edit.py [[path]filename]** - shell to load full screen editor from https://github.com/robert-hh/Micropython-Editor

**bounce.py** - Terminal User Interface demo of a bouncing ball. Modified version of bounce by [DuckyPolice](https://github.com/DuckyPolice)

**xcopy.py[/S][/Y][/V] [path]filename [path][filename]** - a more robust version of the copy command  
- /S Copies specified files from directories and subdirectories, except for empty ones  
- /Y Suppresses prompting to confirm you want to overwrite an existing destination file
- /V Performs a verification read of the copied file to ensure it matches the source

**fileview.py [[path]filename]** - scrollable text file viewer

**sdmount.py [[mount path][,pydos spi bus#]]** - mounts an sd card to the file system. If no SD card CS pins are defined or -1 is passed as the spi bus# the sd
card will be mounted using an SDIO bus rather than an SPI bus.    
**sdumount.py [mount path]** - dismounts an sd card from the file system

**setdate.py [mm-dd-yy]** - initalizes the real time clock to an entered date  
**settime.py [hh:mm:ss]** - initalizes the real time clock to an entered time  
**getdate.py [timzone offset]** (WiFi enabled boards) - sets the time and date from worldtimeapi.org and failing that, uses the Internet NTP protocol

**diff.py [filename1,filename2]** - performs a file comparison

**sound.py [Frequency,Duration(miliseconds),Volume]** - outputs a sound to a speaker cicruit connected to GPIO pin defined in lib/pydos_bcfg.py  
**tsound.py** - test program that plays a short sound sequence  
**piano.py** - emulates a small piano keyboard

**i2cscan.py [bus number]** - scans the I2C bus and displays any found device addresses

CircuitPython LCD libraries from https://github.com/dhylands/python_lcd  
**lcdprint.py [text to display]** - displays text on an I2C LCD display  
**lcdscroll.py [text to scroll]** - scrolls text on an I2C LCD display  
**temperature.py** - displays temperature value from onboard temperature sensor to screen and I2C LCD display

**basicpython.py** - Shell modeled after basic interpreter shell from https://github.com/tannewt/basicpython

**blink.py [led pin number]** - program to blink onboard LED

**rgbset.py [pin number,[size,[pixel]]]** - program to set the rgb color of an onboard neopixel or dotstar. The *size* and *pixel* arguments can be used to identify individual pixel in pixel array of more than 1 neopixel/dotstar.  

**rgbblink.py [pin number]** - program to blink an onboard neopixel or dotstar  
**rgbrainbow.py [pin number]** - program to color cycle an onboard neopixel or dotstar  

**matrix.py [width,height,depth,across,down]** - (Circuitpython only) program to initalize connected HUB75 RGB Matrix Panels as a CircuitPython display. The display object is stored as a PyDOS environment variable (_display).  
  
Parameters:  
width - base width of a single RGB matrix tile  
height - base height of a single RGB matrix tile  
depth - the color depth of the matrix  
across - the number of tiles connected across the matrix display  
down - the number of tiles connected down the matrix display

If the parameters are omitted or not properly formatted, the program will prompt for each of the values.  

**Playimage.py [filename[,filename2,filename3,etc[],seconds_to_display]]]** - (Circuitpython only, requires the adafruit_imageload library installed in the /lib folder) program to display .bmp, .jpg, .gif (incl animated) or .png image files. If multiple comma 
seperated files are entered a continous slide show is displayed with each image being 
displayed for `seconds_to_display` seconds. Wildcard's in the format of *.xxx can be used
as an input filename. If the program is loaded from PyDOS it attempts to determine the appropriate display configuration from the PyDOS environment, otherwise several display options are supported and selected depending on the existence of BOARD.DISPLAY or locally installed display libraries.

**reboot.py** - performs a soft reboot (Micropython requires a Ctrl-D to complete)

**keys.bat** - (Keyboard Featherwing/BBQ Keyboard/LilyGo T-Deck only) Displays keyboard mappings for hidden keys and functions  
**ui.bat [u/k]** - (Keyboard Featherwing/BBQ Keyboard only) Switches between using the Keyboard Featherwing and USB Serial port for PyDOS I/O

**fs.py [ro/rw]** - (Circuitpython only) By selecting the "RO" option the flash mode is set such that when the microcontroller
is power cycled or hard reset, the host computer will have read/write access to the flash and the microcontoller will be
restricted to read only access. To give PyDOS access to the flash after switching to this mode the boot.py file must be
replaced or modified from the host computer so that it contains the following instructions:

    import storage
    storage.remount("/",False)
    
and then power cycled or hard reset.

**setenv.py** - Helper program for adding the WiFi SSID and Password to settings.toml (used by setup.bat).

*WiFi enabled boards only*  
**wifi_finance [symbol]** - Displays the current Nasdaq prices by connecting to a financial website and scraping the information. If an optional symbol is supplied, the program will attempt to identify the symbol and scrap the corresponding price information.  
**wifi_weather** - Displays the 7 day forcast from api.weather.gov

## Hardware (Pin) customization file (pydos_bcfg.py)


The setup.bat file will identify the board being used from **board.board_id** or
**sys.implementation._machine** and attempt to copy a customization file from the cpython or mpython /boardconfigs directory. If a matching config file is not found the default /lib/pydos_bcfg.py file will be used.

The pydos_bcfg.py file acts as a library which contains a single dictionary opject, Pydos_pins.

The recognized keys of the Pydos_pins dictionary are:  

**TUPLES (pin number, Text description of identified pin)**  
example: `'led' : (25, "GP25")`  

**led** - Micropython may use text identifer (i.e. "led") rather than pin number  
**sndPin**  
**neoPixel**  
**neoPixel_Pow**  
**dotStar_Clock**  
**dotStar_Data**  
**dotStar_Extra**  
**dotStar_Pow**  
**I2C_NUM** - MicroPython hardware I2C number  
**SCL**  
**SDA**  
**SDIO_CLK**  
**SDIO_CMD**  
**SDIO_DPINS** - the "pin number" element for SDIO_DPINS is a list of pins  

**LIST OF TUPLES**  
*First tuple in list used for machine/board SD dedicated SPI (board.SD_SPI)*  
*Last tuple in list used for machine/board general use SPI (board.SPI)*  
example: `'MISO' : [(43, "DAT0 D43 Internal"), (12, "MISO D12")]`

**SPI_NUM** - MicroPython hardware SPI number  
**SCK**  
**MOSI**  
**MISO**  
**CS**  

**CALCULATED DATA**

**sndGPIO** - digitalio.DigitalInOut(sndPin)  
**KFW** - Flag indicating use of Keyboard FeatherWing (True/False)  
**I2CbbqDevice** - I2C device being used for the KFW keyboard  
**SD** - list of sdcard objects  
**SDdrive** - list of mount points for mounted SD cards


## PyDOS Generalized Wifi API library (pydos_wifi.py)

Whenever possible PyDOS and the bundled external programs work equally well on MicroPython or CircuitPython and on any of the supported micro controller chip families. To assist in reaching this goal PyDOS_wifi, a simplified Wifi library, is being developed which provides a unified Wifi API that works the same under both MicroPython and CircuitPython on ESP32xx, Pico W and Arduino Nano based Microcontrollers.

For PyDOS_wifi API documentation see https://github.com/RetiredWizard/PyDOS_wifi


## Installation

**Before copying PyDOS files**

If the board you're using has limited flash storage, as is the case with the Pico W, you can delete either the **cpython** (if you're not using CircuitPython) or **mpython**
(if you're not using MicroPython) folder from the downloaded repository files. Within the remaining Python folder (**cpython** or **mpython**) are folders
for specific micro controller boards, you can free up further space by deleting anything other than the board you are using (the "Pico W" and "Arduino Nano Connect" boards use the ESP folder). For very limited Flash boards you may want to delete the **PyBasic** folder until after the **setup.bat** step is run. Once setup has ben run, delete the **cpython** and/or **mpython** folders from the microcontroller and copy as much of the **PyBasic** directory as space permits to the Microcontroller. Copying just the *.py files is all that's needed for PyBasic to run.

**Circuitpython PYSTACK**

Thanks to the great work of **@bill88t**, starting with CircuitPython version 8.0.4, you no longer need to build custom CirucitPython firmware (ESP32 based boards are still being worked on but should have this feature in 8.0.6/8.1.0). PyDOS will run without issue on a standard downloaded CircuitPython image from https://circuitpython.org/downloads. 

When CircuitPython boots on a microcontroller the pystack size can be set by the **CIRCUITPY_PYSTACK_SIZE** value in the settings.toml file. PyDOS comes with this value set to 4000. PyDOS will derive a maximum wildcard length based on this value that should be adequate in most cases, however if you find yourself using particuarly long file names you can increase this parameter value as needed. As you increase the pystack size the memory available for PyDOS to run will decrease slightly.

*By the way, if you like PyDOS you'll probably also enjoy Beryllium OS from https://github.com/beryllium-org/OS  

**CircuitPython install**

To install the CircuitPython image, put your microcontroller board in "bootloader" mode and copy the .UF2 file to the USB mass storage device that shows up on your host computer. 

After the .UF2 file is copied to the microcontroller board it should re-boot and a new USB mass storage device should appear.

**PyDOS install**

*CircuitPython will reboot the microcontroller when it detects files have been changed so by default the microcontroller may restart multiple times during the PyDOS install. This shouln't be a problem, however you can disable the auto-reload feature by updating boot.py. Information and instructions can be found [here](https://learn.adafruit.com/welcome-to-circuitpython/troubleshooting#code-dot-py-restarts-constantly-3108374)*

To copy PyDOS to the microcontroller, simply drag the PyDOS directory structure
(after removing the **mpython** folder if space is a concern) to the root directory of the device that appears on the host computer.

If the copy is interrupted for any reason you can delete the boot.py
file in the root of the microcontroller flash and try the copy again. 

If the copy worked without any errors, you should power cycle the microcontroller board so that the file system is configured to allow the microcontroller to have Read/Write access. When you do this, the host computer will no longer be able to write to the microcontroller mounted drive (usually CIRCUITPY).

If you find yourself locked out of the flash from the host computer and PyDOS is not running, the easiest way to recover is to
connect to the REPL, remove the boot.py file and then power cycle the microcontroller board. 

        import os
        os.remove("boot.py")

To interact with the microcontroller you will need to connect using a terminal program. On a PC you can use putty and on linux, I would recommend [tio](https://github.com/tio/tio). To start tio on linux type the command:

          tio /dev/ttyACM0
	  
You should be presented with either the REPL prompt (>>>) or the PyDOS prompt (\>), if not, press return or Ctrl-C. *After using Thonny, you may need to press CTRL-B to exit the raw REPL mode that 
Thonny uses to transfer and execute files.*

At the REPL prompt type "**import PyDOS**" to start PyDOS. From PyDOS type **setup** to run the customization script.

Once the **setup.bat** script has been run if you have more files to copy to the microcontroller (PyBasic for example) or you want to run **circup**, you will need to give the host computer read/write access to the mounted microcontroller drive. This is done by typing **"fs ro"** at the PyDOS prompt and then power cycling the board.

After running **circup** or deleting/copying files using the Host computer, when you want to run PyDOS normally again, edit the **boot.py** file in the root folder of the mounted microcontroller drive (usually CIRCUITPY) and change the line that reads:  

            storage.remount("/",True)  

to:  

            storage.remount("/",False)  

and then powercycle the board once again.

It is recommended that once the **setup.bat** script has been run, **circup** be run on your host computer, in order to make sure the libraries are updated and in sync with the version of CircuitPython on your microcontroller board.

Instructions on installing and using **circup** can be found [here](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/overview)  

On your host PC, you should run:  
**circup update**  (if you are conected to the board via a USB cable)  
**circup --host *ip-address* --password *CIRCUITPY_WEB_API_PASSWORD* update** (for wifi enabled boards)  
  
On your microcontroller, you can use the **setenv.py** PyDOS program to set or see your current CIRCUITPY_WEB_API_PASSWORD.  

You can also run commands like:
**circup install adafruit_imageload** to install any adafruit libraries you need.  

--------------------------------------------------------------------------------------------------------------------
**Building custom Micropython firmware**

Although you can use a standard Micropython image downloaded from Micropython.org to run PyDOS, there are two reasons you may want to build a custom
Micropython firmware file. 

The first is if you wan to connect up an old school serial terminal to the REPL rather than the standard serial over USB connection. Instructions for building 
Micropython with this modification can be found in section 2.2 of the Raspberry Pi Pico Python SDK at https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf.

The second is that PyDOS uses a recursive routine to process wildcard operations and the default stack in Micropython limits the recursion depth that can be obtained **(With more recent versions of Micropython this has become much less of an issue)**.
This means that PyDOS has to limit wildcard operations, one impact of this is that files with longer file names may not appear
in directory listings when wildcards are used. To eliminate this issue a custom Micropython image can be built with the the MICROPY_STACKLESS parameter in **py/mpconfig.h**
changed from **0** to **1**.  
**\*\*Note\*\* I haven't tested a MICROPY_STACKLESS build since ~1.19**

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

**Note** If the board you're using has an onboard SD card slot, Micropython may not mount the flash at the root mount point. In this case copy the PyDOS files to the "/Flash" folder during the initial PyDOS setup. If you plan to boot your device with an SD card inserted you should install PyDOS and run setup before inserting the SD card, then copy boot.py to the SD card.

**Note** To set up the Seeed (XIAO) nRF52840 board running MicroPython, copy the PyDOS /mpython folder to the /flash folder on the device and then copy the /mpython/boot.py file to /Flash/boot.py and reboot the microcontroller. You should then be able to install PyDOS as usual although the current version of Thonny has difficulty with this board so you should only copy a single folder (i.e. lib, mpython, PyBasic and then all the root files) at a time.

## To Do  
*Possible updates depending on RAM impact*

- ~~integrate ConnectionManager into PyDOS_wifi~~
- investigate porting micropython flash mount to circuitpython
- investigate date/time stamp issue on seeed nrf52840 files
- support for connected color displays  
- ~~support for touch screens~~  
- Rename should allow wildcards in filenames, i.e. "rename *.bas *.txt" or "rename code.py *.sav"  
- Quiet, /Q switches to DEL, RMDIR, COPY, XCOPY commands
- PgUp/PgDwn support in fileview.py
- ~~Properly implement edlin cursor position and append command~~