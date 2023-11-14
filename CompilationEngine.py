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

    def __init__(self, infile) -> None:
        self.token = Tokenizer.JackTokenizer(infile)
        self.writer = VMWriter.VMWriter(infile)

    def advance(self):
        token, value = self.token.advance()
        return (token, value)


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


        self.writer.close()

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

        while self.existStatement():
            if self.nextValueIs("let"): self.compileLet()
            if self.nextValueIs("if"): self.compileIf()
            if self.nextValueIs("while"): self.compileWhile()
            if self.nextValueIs("do"): self.compileDo()
            if self.nextValueIs("return"): self.compileReturn()

    def compileLet(self):
        self.advance() # get 'let'
        tok, name = self.advance() # get varName
        array = self.nextValueIs("[")

        if array:
            kind = self.ST.kindOf(name)
            index = self.ST.indexOf(name)
            self.writer.writePush(segments[kind], index) # push array ptr onto stack
            self.advance() # get '['
            self.compileExpression()
            self.advance() # get ']'
            self.writer.writeArithmetic('add') # base+index push onto stack

        self.advance() # get '='
        self.compileExpression()
        self.advance() # get ';'

        if array:
            self.writer.writePop('temp', 1) # pop expression val into temp
            self.writer.writePop('pointer', 1) # pop base+index into 'that' register
            self.writer.writePush('temp', 1) # push expression back onto stack
            self.writer.writePop('that', 0) # pop value into *(base+index)
        else:
            kind = self.ST.kindOf(name)
            index = self.ST.indexOf(name)
            self.writer.writePop(segments[kind], index) # pop value directly into variable

    labelCount = 0
    def newLabel(self):
        self.labelCount += 1
        return 'label'+str(self.labelCount)

    def compileIf(self):
        endLabel = self.newLabel()

        self.advance() # get if
        self.advance() # get '('
        self.compileExpression()
        self.advance() # get ')'

        self.writer.writeArithmetic('not') # ~(cond)
        notIfLabel = self.newLabel()
        self.writer.writeIf(notIfLabel) # if-goto notIfLabel

        self.advance() # get '{'
        self.compileStatements() # compile if statements
        self.advance() # get '}'

        self.writer.writeGoto(endLabel) # goto label
        self.writer.writeLabel(notIfLabel) # label notIfLabel

        if self.nextValueIs("else"):
            self.advance() # get 'else'
            self.advance() # get '{'
            self.compileStatements() # compile else statements
            self.advance() # get '}'

        self.writer.writeLabel(endLabel) # label endLabel


    def compileWhile(self):
        topLabel = self.newLabel()
        self.writer.writeLabel(topLabel) # label topLabel
        
        self.advance() # get while
        self.advance() # get '('
        self.compileExpression()
        self.advance() # get ')'
        
        self.writer.writeArithmetic('not') # ~(cond)
        notIfLabel = self.newLabel()
        self.writer.writeIf(notIfLabel) # if-goto notIfLabel
        
        self.advance() # get '{'
        self.compileStatements()
        self.advance() # get '}'
        
        self.writer.writeGoto(topLabel) # goto topLabel
        self.writer.writeLabel(notIfLabel) # label notIfLabel


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

        self.compileTerm()
        while self.nextValueIn(self.binaryOp):
            tok, op = self.advance()
            self.compileTerm()
            self.writer.writeArithmetic(arithmetics[op])


    # term: integerConstant | stringConstant | keywordconstant | varName |
    #       varName '['expression']' | subroutineCall | '('expression')' | unaryOp term
    def compileTerm(self):

        if self.nextTokenIs("integerConstant"):
            tok, val = self.advance() # get constant
            self.writer.writePush('constant', val)

        elif self.nextTokenIs("stringConstant"):
            tok, val = self.advance() # get string
            self.writer.writePush('constant', len(val)) # push length of string
            self.writer.writeCall('String.new', 1) # call OS String function w/ 1 argument
            for c in val:
                self.writer.writePush('constant', ord(c)) # push Unicode of character
                self.writer.writeCall('String.appendChar', 2) # call appendChar w/ 2 arguments

        elif self.nextValueIn(self.keywordConstant):
            tok, val = self.advance() # get keyword (true/false/null/this)
            if val == 'true':
                self.writer.writePush('constant', 1)
                self.writer.writeArithmetic('neg')
            elif val == 'this':
                self.writer.writePush('pointer', 0)
            else:
                self.writer.writePush('constant', 0)

        elif self.nextTokenIs("identifier"):

            tok, name = self.advance() # get varName / subroutineCall

            if self.nextValueIs("["):
                self.writeArrayIndex(name)

            elif self.nextValueIs("("):
                nArgs = 1
                self.writer.writePush('pointer', 0) # push this pointer
                name = self.className+'.'+name
                self.advance() # get (
                nArgs += self.compileExpressionList() # VM code to push args
                self.advance() # get )
                self.writer.writeCall(name, nArgs) # call name nArgs

            elif self.nextValueIs("."):
                stype = self.ST.typeOf(name)
                nArgs = 0
                objName = name
                self.advance() # get '.'
                tok, name = self.advance() # get subroutineName

                if stype == None:
                    name = objName+'.'+name # calling using class name
                else:
                    nArgs = 1
                    kind = self.ST.kindOf(objName)
                    index = self.ST.indexOf(objName)
                    self.writer.writePush(segments[kind], index) # push object pointer onto stack
                    name = self.ST.typeOf(objName)+'.'+name

                self.advance() # get (
                nArgs += self.compileExpressionList() # VM code to push args
                self.advance() # get )
                self.writer.writeCall(name, nArgs) # call name nArgs

            else:
                kind = self.ST.kindOf(name)
                index = self.ST.indexOf(name)
                self.writer.writePush(segments[kind], index) # push variable onto stack

        elif self.nextValueIs("("):
            self.advance() # get (
            self.compileExpression()
            self.advance() # get )

        elif self.nextValueIn(self.unaryOp):
            tok, op = self.advance() # get unaryOp
            self.compileTerm()
            if op == '-':
                self.writer.writeArithmetic('neg')
            elif op == '~':
                self.writer.writeArithmetic('not')


    def writeArrayIndex(self, name):
        kind = self.ST.kindOf(name)
        index = self.ST.indexOf(name)
        self.writer.writePush(segments[kind], index) # push array ptr onto stack

        self.advance() # get [
        self.compileExpression() # push index onto stack
        self.advance() # get ]

        self.writer.writeArithmetic('add') # base+index
        self.writer.writePop('pointer', 1) # pop into 'that' ptr
        self.writer.writePush('that', 0) # push *(base+index) onto stack

    def compileExpressionList(self):
        nArgs = 0

        if self.existExpression():
            self.compileExpression()
            nArgs = 1
        while self.nextValueIs(","):
            self.advance() # consume ',' symbol
            self.compileExpression()
            nArgs += 1

        return nArgs

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

