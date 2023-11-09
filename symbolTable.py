#!/usr/bin/env python3


class SymbolTable:
    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3
    
    def __init__(self) -> None:
        pass
    
    def reset(self):
        pass
    
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