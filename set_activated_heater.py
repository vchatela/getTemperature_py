#!/usr/bin/python
import os
import sys
import subprocess

from script import activated_file, writeValueToFile, turnOffHeater, turnOnHeater

writeValueToFile(activated_file,sys.argv[1])
print "Write value %s to %s \n" %(sys.argv[1],activated_file)
if sys.argv[1].lower()=='false':
	turnOffHeater()
elif sys.argv[1].lower()=='true':
	turnOnHeater()
print"\n"