#!/usr/bin/env python3

# Constants for Jack Compiler

# Symbol kinds
STATIC = 0
FIELD = 1
ARG = 2
VAR = 3
NONE = 4

segments = {STATIC:'static', FIELD:'this', ARG:'argument', VAR:'local', NONE:'ERROR'}