#!/usr/bin/env python3


class VMWriter:
    
    def __init__(self, filename) -> None:
        self.outf = open(filename.replace('.jack', '.vm'), "w")
    
    def writePush(self, segment, index):
        self.writeCMD('push', segment, index)
    
    def writePop(self, segment, index):
        self.writeCMD('pop', segment, index)
    
    def writeArithmetic(self, command):
        self.writeCMD(command)
    
    def writeLabel(self, label):
        self.writeCMD('label', label)
    
    def writeGoto(self, label):
        self.writeCMD('goto', label)
    
    def writeIf(self, label):
        self.writeCMD('if-goto', label)
    
    def writeCall(self, name, nArgs):
        self.writeCMD('call', name, nArgs)
    
    def writeFunction(self, name, nVars):
        self.writeCMD('function', name, nVars)
    
    def writeReturn(self):
        self.writeCMD('return')
    
    def close(self):
        self.outf.close()
    
    def writeCMD(self, cmd, arg1='', arg2=''):
        self.outf.write(cmd + ' ' + str(arg1) + ' ' + str(arg2) + '\n')
