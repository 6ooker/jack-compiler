#!/usr/bin/env python3

import jackTokenizer as Tokenizer
import VMWriter
import symbolTable
from JCConstants import *

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

    binaryOp = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}

    def __init__(self, infile, outfile) -> None:
        self.token = Tokenizer.JackTokenizer(infile)
        self.outf = open(outfile, 'w')
        self.alreadyParsedRules = []
        self.indent = ""

    def addIndent(self):
        self.indent += "    "

    def rmIndent(self):
        self.indent = self.indent[:-4]

    def advance(self):
        token, value = self.token.advance()
        return (token, value)

    def writeTerminal(self, token, value):
        self.outf.write(self.indent+"<"+token+"> "+value+" </"+token+">\n")

    def writeNonTerminalOpen(self, rule):
        self.outf.write(self.indent+"<"+rule+">\n")
        self.alreadyParsedRules.append(rule)
        self.addIndent()

    def writeNonTerminalClose(self):
        self.rmIndent()
        rule = self.alreadyParsedRules.pop()
        self.outf.write(self.indent+"</"+rule+">\n")

    def compileClass(self):
        # only creation of SymbolTable
        self.ST = symbolTable.SymbolTable()

        self.advance() # get class
        tok, self.className = self.advance() # get className
        self.advance() # get '{'
        if self.existClassVarDec():
            self.compileClassVarDec()
        while self.existSubroutine():
            self.compileSubroutine()
        self.advance() # get '}'


        self.outf.close()

    def compileClassVarDec(self):
        while self.existClassVarDec():

            token, kvalue = self.advance() # get static / field
            if kvalue is 'static': kvalue = STATIC
            elif kvalue is 'field': kvalue = FIELD
            token, tvalue = self.advance() # get type
            stype = tvalue
            token, nvalue = self.advance() # get varName
            name = nvalue
            self.ST.define(name, stype, kvalue)

            while self.nextValueIs(','):
                self.advance() # get ','
                token, nvalue = self.advance() # get varName
                self.ST.define(nvalue, stype, kvalue)

            self.advance() # get ';'

    def compileSubroutine(self):
        self.ST.reset() # reset (clear) subroutine-level symbol table

        tok, kwd = self.advance() # get constructor / function / method
        if kwd == 'method':
            self.ST.define('this', self.className, ARG)
        self.advance() # get void or type
        self.advance() # get subroutineName
        self.advance() #get '('
        self.compileParameterList()
        self.advance() # get ')'
        self.compileSubroutineBody()


    def compileParameterList(self):

        while self.existParam():
            self.compileParameter()

    def compileParameter(self):
        tok, stype = self.advance() # get type
        tok, name = self.advance() # get varName
        self.ST.define(name, stype, ARG) # add Argument to subroutine level symbol table
        if self.nextValueIs(','):
            self.advance() # get ','

    def compileSubroutineBody(self):

        self.advance() # get '{'
        while self.existVarDec():
            self.compileVarDec()
        self.compileStatements()
        self.advance() # get '}'


    def compileVarDec(self):

        self.advance() # get var
        tok, stype = self.advance() # get type
        tok, name = self.advance() # get varName
        self.ST.define(name, stype, VAR) # add Variable to subroutine level symbol table
        while self.nextValueIs(','):
            self.advance() # get ','
            tok, name = self.advance() # get varName
            self.ST.define(name, stype, VAR) # add further Vars in same line
        self.advance() # get ';'


    def compileStatements(self):
        self.writeNonTerminalOpen("statements")

        while self.existStatement():
            if self.nextValueIs("let"): self.compileLet()
            if self.nextValueIs("if"): self.compileIf()
            if self.nextValueIs("while"): self.compileWhile()
            if self.nextValueIs("do"): self.compileDo()
            if self.nextValueIs("return"): self.compileReturn()

        self.writeNonTerminalClose()

    def compileLet(self):
        self.writeNonTerminalOpen("letStatement")

        self.advance() # get 'let'
        self.advance() # get varName
        if self.nextValueIs("["):
            self.writeArrayIndex() # if array get it
        self.advance() # get '='
        self.compileExpression()
        self.advance() # get ';'

        self.writeNonTerminalClose()

    def compileIf(self):
        self.writeNonTerminalOpen("ifStatement")

        self.advance() # get if
        self.advance() # get '('
        self.compileExpression()
        self.advance() # get ')'
        self.advance() # get '{'
        self.compileStatements()
        self.advance() # get '}'
        if self.nextValueIs("else"):
            self.advance() # get 'else'
            self.advance() # get '{'
            self.compileStatements()
            self.advance() # get '}'

        self.writeNonTerminalClose()

    def compileWhile(self):
        self.writeNonTerminalOpen("whileStatement")

        self.advance() # get while
        self.advance() # get '('
        self.compileExpression()
        self.advance() # get ')'
        self.advance() # get '{'
        self.compileStatements()
        self.advance() # get '}'

        self.writeNonTerminalClose()

    def compileDo(self):
        self.writeNonTerminalOpen("doStatement")

        self.advance() # get do
        self.compileSubroutineCall()
        self.advance() # get ';'

        self.writeNonTerminalClose()

    def compileReturn(self):
        self.writeNonTerminalOpen("returnStatement")

        self.advance() # get return
        while self.existExpression():
            self.compileExpression()
        self.advance() # get ';'

        self.writeNonTerminalClose()

    def compileSubroutineCall(self):
        self.advance() # get subroutineName / className / varName
        if self.nextValueIs("."): # case Name.subroutine
            self.advance() # get '.'
            self.advance() # get subroutineName
        self.advance() # get '('
        self.compileExpressionList()
        self.advance() # get ')'

    # expression: term(op term)*
    def compileExpression(self):
        self.writeNonTerminalOpen("expression")

        self.compileTerm()
        if self.nextValueIn(self.binaryOp):
            self.advance() # get Op token
            self.compileTerm()

        self.writeNonTerminalClose()

    # term: integerConstant | stringConstant | keywordconstant | varName |
    #       varName '['expression']' | subroutineCall | '('expression')' | unaryOp term
    def compileTerm(self):
        self.writeNonTerminalOpen("term")

        if self.nextTokenIs("integerConstant") or\
            self.nextTokenIs("stringConstant") or \
            self.nextValueIn(self.keywordConstant):

                self.advance() # get constant

        elif self.nextTokenIs("identifier"):

            self.advance() # get varName / subroutineCall

            if self.nextValueIs("["):
                self.writeArrayIndex()

            if self.nextValueIs("("):
                self.advance() # get (
                self.compileExpressionList()
                self.advance() # get )

            if self.nextValueIs("."):
                self.advance() # get '.'
                self.advance() # get subroutineName
                self.advance() # get (
                self.compileExpressionList()
                self.advance() # get )

        elif self.nextValueIs("("):
            self.advance() # get (
            self.compileExpression()
            self.advance() # get )

        elif self.nextValueIn(self.unaryOp):
            self.advance() # get unaryOp
            self.compileTerm()

        self.writeNonTerminalClose()

    def writeArrayIndex(self):
        self.advance() # get [
        self.compileExpression()
        self.advance() # get ]

    def compileExpressionList(self):
        self.writeNonTerminalOpen("expressionList")

        if self.existExpression():
            self.compileExpression()
        while self.nextValueIs(","):
            self.advance() # consume ',' symbol
            self.compileExpression()

        self.writeNonTerminalClose()

    def existExpression(self):
        return self.existTerm()

    def existTerm(self):
        token, value = self.token.peek()
        return self.nextTokenIs("integerConstant") or self.nextTokenIs("stringConstant") or\
                (self.nextValueIn(self.keywordConstant)) or self.nextTokenIs("identifier") or\
                (self.nextValueIn(self.unaryOp)) or self.nextValueIs("(")

    def existStatement(self):
        return self.nextValueIs("let") or self.nextValueIs("if") or\
                self.nextValueIs("while") or self.nextValueIs("do") or\
                self.nextValueIs("return")

    def existClassVarDec(self):
        return self.nextValueIs("static") or self.nextValueIs("field")

    def existSubroutine(self):
        return self.nextValueIs("constructor") or self.nextValueIs("function") or self.nextValueIs("method")

    def existParam(self):
        return not self.nextTokenIs("symbol")

    def existVarDec(self):
        return self.nextValueIs("var")

    def nextValueIs(self, val):
        token, value = self.token.peek()
        return value == val

    def nextTokenIs(self, tok):
        token, value = self.token.peek()
        return token == tok

    def nextValueIn(self, _list):
        token, value = self.token.peek()
        return value in _list

