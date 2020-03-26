#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
# program = sys.argv[1]
cpu = CPU()

cpu.load("examples/stack.ls8") #removed program for testing, examples/mult.ls8 for testing
cpu.run()
