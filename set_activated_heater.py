#!/usr/bin/python
import os
import sys
import subprocess

from script import activated_file, writeValueToFile

global activated_file


wiring_pin_rpi = 29
action_command_turn_off = '/var/www/hcc/radioEmission '+str(wiring_pin_rpi)+' 12325261 1 off'

writeValueToFile(activated_file,sys.argv[1])
print "Activated = %s" %sys.argv[1]
if sys.argv[1]=='False' or sys.argv[1]=='false' :
	print "turn off heater" 
	subprocess.call(action_command_turn_off, shell=True)
	writeValueToFile(is_on_heater,'False')