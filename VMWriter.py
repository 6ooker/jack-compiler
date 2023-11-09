#!/usr/bin/env python3


class VMWriter:
    
    def __init__(self) -> None:
        pass
    
    def writePush(self, segment, index):
        pass
    
    def writePop(self, segment, index):
        pass
    
    def writeArithmetic(self, command):
        pass
    
    def writeLabel(self, label):
        pass
    
    def writeGoto(self, label):
        pass
    
    def writeIf(self, label):
        pass
    
    def writeCall(self, name, nArgs):
        pass
    
    def writeFunction(self, name, nVars):
        pass
    
    def writeReturn(self):
        pass
    
    def close(self):
        pass