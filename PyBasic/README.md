# A BASIC Interpreter - Program like it's 1979!

Basic interpreter copied from https://github.com/richpl/PyBasic and modified to run under Micropython, CircuitPython or cPython under Windows. The interpreter can be launched from PyDOS by typing "PyBasic" or from the REPL by typing "import PyBasic"

**There has been a great deal of work done recently to bring most of the changes in the PyDOS version of PyBasic to the original RICHPL version. See the excellent PyBasic documentation at https://github.com/richpl/PyBasic#readme**


The PyDOS version of PyBasic still has the following difference from the richpl github version:

* PyDOS command line argument functionality 
* prompt changed from > to :
* commas can be used in addition to semi-colons as print statment delimeters
* TAB() function places print cursor at specified column rather than inserting specified number of spaces
* starting array element 1 rather than 0, so that dim(10) created a 10 element array
* PI, RNDINT, TERNARY, LEFT$, RIGHT$ functions not supported in PyDOS version

* PyDOS version runs Basic program in place on disk rather than loading into memory
* added a saved index source code option when saving or loading using the .PGM extension on a program filename, this vastly speeds up subsequent program load times

* pre-allocation of memory on startup, this seems to reduce the memory allocation errors when attempting to run large basic programs

* added SOUND freq,duration[,volume] command. The Windows code uses the winsound library and the Micropython/Circuit Python implementations
         assumes the appropriate speaker circuit is connected to GPIO pin #19

