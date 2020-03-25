#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
# program = sys.argv[1]
cpu = CPU()

cpu.load("examples/mult.ls8") #removed program for testing
cpu.run()
