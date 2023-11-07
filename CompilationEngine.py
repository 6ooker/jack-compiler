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
    
    binaryOp = {'+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '='}
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
        self.writeTerminal(token, value)
        
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
        self.writeNonTerminalOpen("statements")
        
        while self.existStatement():
            if self.nextValueIs("let"): self.compileLet()
            if self.nextValueIs("if"): self.compileIf()
            if self.nextValueIs("while"): self.compileWhile()
            if self.nextValueIs("do"): self.compileDo()
            if self.nextValueIs("return"): self.compileReturn()
        
        self.writeNonTerminalClose()
    
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
    
    def nextValueIs(self, val):
        token, value = self.token.peek()
        return value == val

    def nextTokenIs(self, tok):
        token, value = self.token.peek()
        return token == tok
    
    def nextValueIn(self, _list):
        token, value = self.token.peek()
        return value in _list

