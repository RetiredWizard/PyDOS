Basic interpreter copied from https://github.com/richpl/PyBasic and modified to run under Micropython, CircuitPython
cPython under Windows. The interpreter can be launched from PyDOS by typing "PyBasic" or from the REPL by typing "import PyBasic"


The following changes have been made to the richpl github version:


* save and load from text file rather than pickle binary
* added command line argument functionality 
* prompt changed from > to :
* added functionality to LIST command allow the specification of line or line range
* added single line compound statement support with : seperator
* change print delimeter from : to ; or ,
* added trailing ; to print statement to indicate print without end carriage return
* added TAB() function support to print statement
* added memory garbage collection before array creation attempts
* modified starting array element from 0 to 1 so that dim(10) created a 10 element array
* attempted to resolve branching out of active loop with goto and then returning to start of loop problem
* PI, RNDINT, TERNARY functions removed
* VAL function modified slightly to work on micropython

* modified PyBasic to run Basic program in place on disk rather loading into memory
* added logic to allow this version of PyBasic to run on Windows platform in cPython as well as micro python
* added logic to allow tab() function to work across print statements continued with trailing ;
* added logic to ignore null tokens caused by trailing spaces
* added logic to prevent text of REM statements being evaluated as tokens and syntax checked

* modified mid$(s$,S,L) function so that an 'S' of 1 indicated the first char (not 0) of the substring and 'L' is
        the length rather than the ending position
* modified INSTR to count the first string position as 1 instead of 0 and return a 0 if not found rather than -1
* added file I/O ('OPEN fn FOR access-type AS #f ELSE lineno', 'INPUT #f', 'PRINT #f', 'FSEEK #f,pos', 'CLOSE #f')
* added 'RESTORE lineno' command to DATA/read functionality
* modified the 'ON val GOTO/GOSUB line1,line2,...' to function in a more standard way
* added a saved index source code option when saving or loading using the .PGM extension on a program filename

* pre-allocation of memory on startup, this seems to reduce the memory allocation errors when attempting to run large basic programs

* added SOUND freq,duration[,volume] command. The Windows code uses the winsound library and the Micropython implementation
         assumes the appropriate speaker circuit is connected to GPIO pin #20 

