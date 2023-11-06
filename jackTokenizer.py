#!/usr/bin/env python3

import re

# keywords:         class constructor function method field static var int char
#                   boolean void true false null this let do if else while return
# symbols:          { } ( ) [ ] . , ; + - * / & | < > = ~
# integerConstant:  decimal number in range 0..32767
# StringConstant:   "Unicode char sequence not including double quotes or newline"
# identifier:       sequence of letters, digits and underscore _ not starting w/ digit

class JackTokenizer:
    KEYWORD = 0
    SYMBOL = 1
    INTCONST = 2
    STRCONST = 3
    IDENTIFIER = 4

    def __init__(self, infile) -> None:
        file = open(infile, 'r')
        self._lines = file.read()
        self.removeComments()
        self.current_token = ''
        self._init_token_info()

    def __str__(self) -> str:
        pass
    
    def _init_token_info(self):
        self._tokenType = -1
    
    def hasMoreTokens(self) -> bool:
        return self._tokens != []
    
    def advance(self):
        self._init_token_info()
        self.current_token = self._tokens.pop(0)
        
    def removeComments(self):
        currentIndex = 0
        endIndex = 0
        filteredText = ''
        
        while currentIndex < len(self._lines):
            currentChar = self._lines[currentIndex]
            
            if currentChar == "\"":
                endIndex = self._lines.find("\"", currentIndex + 1)
                filteredText += self._lines[currentIndex:endIndex+1]
                currentIndex = endIndex + 1
                
            elif currentChar == "/":
                if self._lines[currentIndex + 1] == "/":
                    endIndex = self._lines.find("\n", currentIndex + 1)
                    currentIndex = endIndex + 1
                    filteredText += " "
                elif self._lines[currentIndex + 1] == "*":
                    endIndex = self._lines.find("*/", currentIndex + 1)
                    currentIndex = endIndex + 2
                    filteredText += " "
                else:
                    filteredText += self._lines[currentIndex]
                    currentIndex += 1
            else:
                filteredText += self._lines[currentIndex]
                currentIndex += 1
        self._lines = filteredText
        return
    
    
    
    def tokenType(self):
        pass
    
    
    def keyWord(self):
        pass
    
    def symbol(self):
        pass
    
    def identifier(self):
        pass
    
    def intVal(self):
        pass
    
    def stringVal(self):
        pass
    

j = JackTokenizer('./Main.jack')
print(j._lines)