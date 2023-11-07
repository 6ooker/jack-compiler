#!/usr/bin/env python3

import jackTokenizer as Tokenizer

# program structure:
# class: 'class' className '{' classVarDec* subroutineDec* '}'
# classVarDec: ('static'|'field') type varName (',' varName)* ';'
# type: 'int'|'char'|'boolean'|className
# subroutineDec: ('constructor'|'function'|'method') ('void'|type)subroutineName '('parameterList')' subroutineBody
# parameterList: ((type varName) (',' type varName)*)?
# subroutineBody: '{' varDec* statements '}'
# varDec: 'var' type varName (',' varName)* ';'
# className: identifier
# subroutineName: identifier
# varName: identifier

class CompilationEngine:
    
    def __init__(self, infile, outfile) -> None:
        self.tok = Tokenizer.JackTokenizer(infile)
    
    def compileClass(self):
        pass
    
    def compileClassVarDec(self):
        pass
    
    def compileSubroutine(self):
        pass
    
    def compileParameterList(self):
        pass
    
    def compileSubroutineBody(self):
        pass
    
    def compileVarDec(self):
        pass
    
    def compileStatements(self):
        pass
    
    def compileLet(self):
        pass
    
    def compileIf(self):
        pass
    
    def compileWhile(self):
        pass
    
    def compileDo(self):
        pass
    
    def compileReturn(self):
        pass
    
    def compileExpression(self):
        pass
    
    def compileTerm(self):
        pass
    
    def compileExpressionList(self):
        pass
    
    def eat(self, string):
        if (not string in self.tok.current_token):
            raise Exception("Token Error")
        else:
            self.tok.advance()

