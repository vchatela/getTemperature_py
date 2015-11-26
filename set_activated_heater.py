#!/usr/bin/python
import os
import sys
import subprocess

from script import activated_file, writeValueToFile, wiring_pin_rpi, action_command_turn_off

dir_temp_file = '/var/www/files'
is_on_heater = dir_temp_file + '/is_on_heater'

writeValueToFile(activated_file,sys.argv[1])
print "Activated = %s" %sys.argv[1]
if sys.argv[1]=='False' or sys.argv[1]=='false' :
	print "turn off heater" 
	subprocess.call(action_command_turn_off, shell=True)
	print "Write False to the is_on_heater file"
	writeValueToFile(is_on_heater,'False')