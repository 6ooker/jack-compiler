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

    def define(self, name, stype, kind):
        self.symbols[kind][name] = (stype, kind, self.index[kind])
        self.index[kind] += 1

    def varCount(self, kind) -> int:
        return sum(1 for n, (t, k, i) in self.symbols[kind].items() if k == kind)

    def kindOf(self, name):
        (stype, kind, index) = self.lookup(name)
        return kind

    def typeOf(self, name) -> str:
        (stype, kind, index) = self.lookup(name)
        return stype

    def indexOf(self, name) -> int:
        (stype, kind, index) = self.lookup(name)
        return index

    def lookup(self, name) -> tuple:
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name]
        elif name in self.class_symbols:
            return self.class_symbols[name]
        else:
            return (None, None, None)
