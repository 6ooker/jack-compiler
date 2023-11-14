#!/usr/bin/env python3

import CompilationEngine
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 jackAnalyzer.py 'file.jack' or dir")
    else:
        instream = sys.argv[1]

    # Handling if given single .jack file
    if os.path.isfile(instream):
        if not os.path.basename(instream).endswith('.jack'):
            raise Exception("Must provide dir or single .jack file")

        CE = CompilationEngine.CompilationEngine(instream)
        CE.compileClass()

    elif os.path.isdir(instream):
        for jackFile in [f for f in os.listdir(instream) if f.endswith('.jack')]:
            infile = os.path.join(instream, jackFile)
            CE = CompilationEngine.CompilationEngine(infile)
            CE.compileClass()


main()