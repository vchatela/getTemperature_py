#!/usr/bin/python
import os
import sys

from script import activated_file, writeValueToFile

global activated_file

writeValueToFile(activated_file,sys.argv[1])
print "Activated = %s" %sys.argv[1]

