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

"""Class representing a BASIC DATA Statements.
This is a list of DATA statements, ordered by
line number.

"""

from basictoken import BASICToken as Token
from lexer import Lexer

class BASICData:

    def __init__(self):
        # Dictionary to represent data
        # statements, keyed by line number
        self.__data = {}

        # Data pointer
        self.__next_data = 0

    def delete(self):
        self.__data.clear()
        self.__next_data = 0

    def delData(self,line_number):
        if self.__data.get(line_number) != None:
            del self.__data[line_number]

    def addData(self,line_number,fIndex):
        """
        Adds the supplied token list
        to the program's DATA store. The first token should
        be the line number. If a token list with the
        same line number already exists, this is
        replaced.

        line_number: Basic program line number of DATA statement
        fIndex: if >= 0: location in loaded program file of statment
                if < 0: Location in temporary basic workfile

        """

        try:
            self.__data[line_number] = fIndex

        except TypeError as err:
            raise TypeError("Invalid line number: " + str(err))

    def readData(self,read_line_number,infile,tmpfile):

        if len(self.__data) == 0:
            raise RuntimeError('No DATA statements available to READ ' +
                               'in line ' + str(read_line_number))

        data_values = []

        line_numbers = list(self.__data.keys())
        line_numbers.sort()
        #print("+++",self.__next_data,line_numbers)


        if self.__next_data == 0:
            self.__next_data = line_numbers[0]
        elif line_numbers.index(self.__next_data) < len(line_numbers)-1:
            self.__next_data = line_numbers[line_numbers.index(self.__next_data)+1]
        else:
            raise RuntimeError('No DATA statements available to READ ' +
                               'in line ' + str(read_line_number))

        if self.__data[self.__next_data] >= 0:
            infile.seek(self.__data[self.__next_data])
            tokenlist = Lexer().tokenize((infile.readline().replace("\n","")).replace("\r",""))[1:]
        else:
            tmpfile.seek(-(self.__data[self.__next_data]+1))
            tokenlist = Lexer().tokenize((tmpfile.readline().replace("\n","")).replace("\r",""))[1:]

        sign = 1
        for token in tokenlist[1:]:
            if token.category != Token.COMMA:
                if token.category == Token.STRING:
                    data_values.append(token.lexeme)
                elif token.category == Token.UNSIGNEDINT:
                    data_values.append(sign*int(token.lexeme))
                elif token.category == Token.UNSIGNEDFLOAT:
                    data_values.append(sign*eval(token.lexeme))
                elif token.category == Token.MINUS:
                    sign = -1
                #else:
                    #data_values.append(token.lexeme)
            else:
                sign = 1


        return data_values

    def restore(self,restoreLineNo):
        if restoreLineNo == 0 or self.__data.get(restoreLineNo) != None:

            if restoreLineNo == 0:
                self.__next_data = restoreLineNo
            else:

                line_numbers = list(self.__data.keys())
                line_numbers.sort()

                indexln = line_numbers.index(restoreLineNo)

                if indexln == 0:
                    self.__next_data = 0
                else:
                    self.__next_data = line_numbers[indexln-1]
        else:
            raise RuntimeError('Attempt to RESTORE but no DATA ' +
                               'statement at line ' + str(restoreLineNo))