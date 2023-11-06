#!/usr/bin/env python3

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
        self.infile = infile
    
    def hasMoreTokens(self):
        pass
    
    def advance(self):
        pass
    
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
    