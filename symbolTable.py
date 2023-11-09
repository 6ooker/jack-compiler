#!/usr/bin/env python3

from JCConstants import *

class SymbolTable:

    
    def __init__(self) -> None:
        self.class_symbols = {}
        self.subroutine_symbols = {}
        self.symbols = {STATIC:self.class_symbols, FIELD:self.class_symbols,
                        ARG:self.subroutine_symbols, VAR:self.subroutine_symbols}
        self.index = {STATIC:0, FIELD:0, ARG:0, VAR:0}
    
    def reset(self):
        self.subroutine_symbols.clear()
        self.index[STATIC] = self.index[VAR] = 0
    
    def define(self, name, type, kind):
        pass
    
    def varCount(self, kind) -> int:
        pass
    
    def kindOf(self, name):
        pass
    
    def typeOf(self, name) -> str:
        pass
    
    def indexOf(self, name) -> int:
        pass