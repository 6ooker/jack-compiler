#!/usr/bin/env python3

import re

# keywords:         class constructor function method field static var int char
#                   boolean void true false null this let do if else while return
# symbols:          { } ( ) [ ] . , ; + - * / & | < > = ~
# integerConstant:  decimal number in range 0..32767
# StringConstant:   "Unicode char sequence not including double quotes or newline"
# identifier:       sequence of letters, digits and underscore _ not starting w/ digit

class JackTokenizer:
    KeywordsCodes = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
    SymbolsCodes = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}

    def __init__(self, infile) -> None:
        file = open(infile, 'r')
        self._lines = file.read()
        self.removeComments()
        self.tokens = self.tokenize()
        self.current_token = ''

    def __str__(self) -> str:
        pass
    
    def hasMoreTokens(self) -> bool:
        return self.tokens != []
    
    def advance(self):
        self.current_token = self.tokens.pop(0)
        return self.current_token
        
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
    
    
    keywordsRegex = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    symbolsRegex = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    integersRegex = r'\d+'
    stringsRegex = r'"[^"\n]*"'
    identifiersRegex = r'[\w]+'
    word = re.compile(keywordsRegex + '|' + symbolsRegex + '|' + integersRegex + '|' + stringsRegex + '|' + identifiersRegex)
    
    def token(self, word):
        if re.match(self.keywordsRegex, word) != None: return ("keyword", word)
        elif re.match(self.symbolsRegex, word) != None: return ("symbol", word)
        elif re.match(self.integersRegex, word) != None: return ("integerConstant", word)
        elif re.match(self.stringsRegex, word) != None: return ("stringConstant", word[1:-1])
        else:                                           return ("identifier", word)
    
    def tokenize(self):
        return [self.token(word) for word in self.split(self._lines)]
    
    def split(self, line):
        return self.word.findall(line)
    
    def tokenType(self):
        return self.current_token[0]
    
    def tokenValue(self):
        return self.current_token[1]
    
