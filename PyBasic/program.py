#! /usr/bin/python

# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Class representing a BASIC program.
This is a list of statements, ordered by
line number.

"""

from basicdata import BASICData
from basictoken import BASICToken as Token
from basicparser import BASICParser
from flowsignal import FlowSignal
from lexer import Lexer
import gc
from os import listdir,remove
from sys import implementation
try:
    from pydos_ui import input
except:
    pass
gc.collect()

class Program:

    def __init__(self):
        # Dictionary to represent program
        # statements, keyed by line number
        self.__program = {}

        # Program counter
        self.__next_stmt = 0

        # Initialise return stack for subroutine returns
        self.__return_stack = []

        # return dictionary for loop returns
        self.__return_loop = {}

        # Setup DATA object
        self.__data = BASICData()

    def list(self, strt_line, end_line, infile, tmpfile):
        """Lists the program"""
        line_numbers = self.line_numbers()

        for line_number in line_numbers:
            if (int(line_number) >= strt_line and int(line_number) <= end_line) or strt_line == -1:
                print(line_number, end=' ')

                statement = self.getprogram(line_number,infile,tmpfile)
                for token in statement:
                    # Add in quotes for strings
                    if token.category == Token.STRING:
                        print('"' + token.lexeme + '"', end=' ')

                    else:
                        print(token.lexeme, end=' ')

                print()

    def save(self, file, infile, tmpfile):
        """Save the program

        :param file: The name and path of the save file

        """
        retCode = False

        ans = "Y"
        if file in listdir():
            ans = input("Overwrite "+file+" (y/n): ").upper()

        if ans == "Y":

            if file+".pYb" in listdir():
                remove(file+".pYb")

            try:
                with open(file+".pYb", 'w') as outfile:

                    line_numbers = self.line_numbers()

                    if file.split(".")[-1].upper() == "PGM":
                        filelen = 0
                        for line_number in line_numbers:
                            statement = self.getprogram(line_number,infile,tmpfile)
                            if len(statement) > 1 and statement[0].lexeme == "DATA":
                                sign = -1
                            else:
                                sign = 1
                            fileLine = str(line_number)+","+str(sign*self.__program[line_number])
                            outfile.write(fileLine+"\n")
                            filelen += (len(fileLine)+(0 if implementation.name.upper() in ['MICROPYTHON','CIRCUITPYTHON'] else 1))
                        outfile.write("-999,-999\n")
                        filelen += (10 if implementation.name.upper() in ['MICROPYTHON','CIRCUITPYTHON'] else 11)

                    for line_number in line_numbers:
                        fileLine = str(line_number)

                        statement = self.getprogram(line_number,infile,tmpfile)
                        for token in statement:
                            # Add in quotes for strings
                            if token.category == Token.STRING:
                                fileLine += ' "' + token.lexeme + '"'

                            else:
                                fileLine += " " + token.lexeme
                        outfile.write(fileLine+"\n")

                retCode = True

            except OSError:
                print("Could not save to file")

        return retCode

    def load(self, file, tmpfile):
        """Load the program

        :param file: The name and path of the file to be loaded
        tmpfile:     File handle for temporary basic workfile"""

        infile = None

        try:
            infile = open(file, 'r')
            fIndex = 0
            fOffset = 0
            pgmLoad = False
            if file.split(".")[-1].upper() == "PGM":
                pgmLoad = True
                for fileLine in infile:
                    fOffset += (len(fileLine) + (0 if implementation.name.upper() in ['MICROPYTHON','CIRCUITPYTHON'] else 1))
                    if len(fileLine) >= 9 and fileLine[0:9] == "-999,-999":
                        break

            infile.seek(0)
            for fileLine in infile:
                if pgmLoad:
                    line_number = int(fileLine.split(",")[0])
                    fIndex = int(fileLine.split(",")[1])
                    if len(fileLine) >= 9 and fileLine[0:9] == "-999,-999":
                        break
                    self.__program[line_number] = abs(fIndex)+fOffset
                    if fIndex < 0:
                        self.__data.addData(line_number,abs(fIndex)+fOffset)
                else:
                    if ((fileLine.strip()).replace("\n","")).replace("\r","") != "":
                        line_number = int(fileLine.strip().split(" ")[0])
                        self.__program[line_number] = fIndex+fOffset
                        if fileLine.strip().upper()[fileLine.strip().find(' '):].strip()[:4] == "DATA":
                            self.__data.addData(line_number,fIndex)
                        #self.add_stmt(Lexer().tokenize((fileLine.replace("\n","")).replace("\r","")),fIndex+fOffset,tmpfile)
                    fIndex += (len(fileLine) + (0 if implementation.name.upper() in ['MICROPYTHON','CIRCUITPYTHON'] else 1))


        except OSError:
            print("Could not read file")

        return infile

    def add_stmt(self, tokenlist, fIndex, tmpfile):
        """
        Adds the supplied token list
        to the program. The first token should
        be the line number. If a token list with the
        same line number already exists, this is
        replaced.

        :param tokenlist: List of BTokens representing a
        numbered program statement
        fIndex: if >= 0: location in loaded program file of statment
                if < 0: Indicates statement was not read and should
               be added to temporary basic workfile
        tmpfile: file handle of temporary basic workfile

        """
        try:
            line_number = int(tokenlist[0].lexeme)
            if fIndex >= 0:
                self.__program[line_number] = fIndex
                if tokenlist[1].lexeme == "DATA":
                    self.__data.addData(line_number,fIndex)
            else:
                tmpfile.seek(0)
                filelen = 0
                for lines in tmpfile:
                    filelen += (len(lines)+(0 if implementation.name.upper() in ['MICROPYTHON','CIRCUITPYTHON'] else 1))

                self.__program[line_number] = -(filelen+1)
                if tokenlist[1].lexeme == "DATA":
                    self.__data.addData(line_number,-(filelen+1))
                #self.__program[line_number] = -(len(tmpfile.read())+1)

                fileLine = str(line_number)
                for token in tokenlist[1:]:
                    # Add in quotes for strings
                    if token.category == Token.STRING:
                        fileLine += ' "' + token.lexeme + '"'
                    else:
                        fileLine += " " + token.lexeme
                tmpfile.write(fileLine+"\n")

        except TypeError as err:
            raise TypeError("Invalid line number: " +
                            str(err))

    def line_numbers(self):
        """Returns a list of all the
        line numbers for the program,
        sorted

        :return: A sorted list of
        program line numbers
        """
        line_numbers = list(self.__program.keys())
        line_numbers.sort()

        return line_numbers

    def getprogram(self, ln, infile, tmpfile):
        if self.__program[ln] >= 0:
            infile.seek(self.__program[ln])
            statement = Lexer().tokenize((infile.readline().strip().replace("\n","")).replace("\r",""))[1:]
        else:
            tmpfile.seek(-(self.__program[ln]+1))
            statement = Lexer().tokenize((tmpfile.readline().replace("\n","")).replace("\r",""))[1:]

        return statement

    def __execute(self, line_number, infile,tmpfile):
        """Execute the statement with the
        specified line number

        :param line_number: The line number

        :return: The FlowSignal to indicate to the program
        how to branch if necessary, None otherwise

        """
        if line_number not in self.__program.keys():
            raise RuntimeError("Line number " + line_number +
                               " does not exist")

        statement = self.getprogram(line_number,infile,tmpfile)

        number_of_stmts = 1
        for e in statement:
            if e.category == Token.COLON:
                number_of_stmts += 1
            elif e.category == Token.IF:
                # any colons after an IF statement are seperators for the THEN or ELSE clause
                # and will be processed by the recursive call to PARSE within the PARSE method
                break

        for cstmt_number in range(0,number_of_stmts):
            try:
            #if True:
                tmp_flow = self.__parser.parse(statement, line_number, cstmt_number, infile, tmpfile, self.__data)

            except RuntimeError as err:
                raise RuntimeError(str(err))

            except KeyboardInterrupt:
                return FlowSignal(ftype=FlowSignal.STOP)

            if tmp_flow:
                break

        return tmp_flow


    def execute(self,infile,tmpfile):
        """Execute the program"""

        self.__parser = BASICParser()

        self.__data.restore(0) # reset data pointer

        line_numbers = self.line_numbers()

        if len(line_numbers) > 0:
            # Set up an index into the ordered list
            # of line numbers that can be used for
            # sequential statement execution. The index
            # will be incremented by one, unless modified by
            # a jump
            index = 0
            self.set_next_line_number(line_numbers[index])

            # Run through the program until the
            # has line number has been reached
            while True:
                flowsignal = self.__execute(self.get_next_line_number(),infile,tmpfile)
                self.__parser.last_flowsignal = flowsignal


                if flowsignal:
                    if flowsignal.ftype == FlowSignal.SIMPLE_JUMP:
                        # GOTO or conditional branch encountered
                        try:
                            index = line_numbers.index(flowsignal.ftarget)

                        except ValueError:
                            raise RuntimeError("Invalid line number supplied in GOTO or conditional branch: "
                                               + str(flowsignal.ftarget)+ " in line " + str(self.get_next_line_number()))

                        self.set_next_line_number(flowsignal.ftarget)

                    elif flowsignal.ftype == FlowSignal.GOSUB:
                        # Subroutine call encountered
                        # Add line number of next instruction to
                        # the return stack
                        if index + 1 < len(line_numbers):
                            self.__return_stack.append(line_numbers[index + 1])

                        else:
                            raise RuntimeError("GOSUB at end of program, nowhere to return")

                        # Set the index to be the subroutine start line
                        # number
                        try:
                            index = line_numbers.index(flowsignal.ftarget)

                        except ValueError:
                            raise RuntimeError("Invalid line number supplied in subroutine call: "
                                               + str(flowsignal.ftarget))

                        self.set_next_line_number(flowsignal.ftarget)

                    elif flowsignal.ftype == FlowSignal.RETURN:
                        # Subroutine return encountered
                        # Pop return address from the stack
                        try:
                            index = line_numbers.index(self.__return_stack.pop())

                        except ValueError:
                            raise RuntimeError("Invalid subroutine return in line " +
                                               str(self.get_next_line_number()))

                        except IndexError:
                            raise RuntimeError("RETURN encountered without corresponding " +
                                               "subroutine call in line " + str(self.get_next_line_number()))

                        self.set_next_line_number(line_numbers[index])

                    elif flowsignal.ftype == FlowSignal.STOP:
                        break

                    elif flowsignal.ftype == FlowSignal.LOOP_BEGIN:
                        # Loop start encountered
                        # Put loop line number on the stack so
                        # that it can be returned to when the loop
                        # repeats
                        self.__return_loop[flowsignal.floop_var] = self.get_next_line_number()

                        # Continue to the next statement in the loop
                        index = index + 1

                        if index < len(line_numbers):
                            self.set_next_line_number(line_numbers[index])

                        else:
                            # Reached end of program
                            raise RuntimeError("Program terminated within a loop")

                    elif flowsignal.ftype == FlowSignal.LOOP_SKIP:
                        # Loop variable has reached end value, so ignore
                        # all statements within loop and move past the corresponding
                        # NEXT statement
                        index = index + 1
                        while index < len(line_numbers):
                            next_line_number = line_numbers[index]
                            #temp_tokenlist = self.__program[next_line_number]
                            temp_tokenlist = self.getprogram(next_line_number,infile,tmpfile)

                            if temp_tokenlist[0].category == Token.NEXT and \
                               len(temp_tokenlist) > 1:
                                # Check the loop variable to ensure we have not found
                                # the NEXT statement for a nested loop
                                if temp_tokenlist[1].lexeme == flowsignal.ftarget:
                                    # Move the statement after this NEXT, if there
                                    # is one
                                    index = index + 1
                                    if index < len(line_numbers):
                                        next_line_number = line_numbers[index]  # Statement after the NEXT
                                        self.set_next_line_number(next_line_number)
                                        break

                            index = index + 1

                        # Check we have not reached end of program
                        if index >= len(line_numbers):
                            # Terminate the program
                            break

                    elif flowsignal.ftype == FlowSignal.LOOP_REPEAT:
                        # Loop repeat encountered
                        # Pop the loop start address from the stack
                        try:
                            index = line_numbers.index(self.__return_loop.pop(flowsignal.floop_var))

                        except ValueError:
                            raise RuntimeError("Invalid loop exit in line " +
                                               str(self.get_next_line_number()))

                        except KeyError:
                            raise RuntimeError("NEXT encountered without corresponding " +
                                               "FOR loop in line " + str(self.get_next_line_number()))

                        self.set_next_line_number(line_numbers[index])

                else:
                    index = index + 1

                    if index < len(line_numbers):
                        self.set_next_line_number(line_numbers[index])

                    else:
                        # Reached end of program
                        break

        else:
            raise RuntimeError("No statements to execute")

    def delete(self):
        """Deletes the program by emptying the dictionary"""
        self.__program.clear()
        self.__data.delete()

    def delete_statement(self, line_number):
        """Deletes a statement from the program with
        the specified line number, if it exists

        :param line_number: The line number to be deleted

        """

        self.__data.delData(line_number)

        try:
            del self.__program[line_number]

        except KeyError:
            raise KeyError("Line number does not exist")

    def get_next_line_number(self):
        """Returns the line number of the next statement
        to be executed

        :return: The line number

        """

        return self.__next_stmt

    def set_next_line_number(self, line_number):
        """Sets the line number of the next
        statement to be executed

        :param line_number: The new line number

        """
        self.__next_stmt = line_number
