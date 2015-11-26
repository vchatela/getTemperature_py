#!/usr/bin/python
import os
import sys
import subprocess

from script import activated_file, writeValueToFile, wiring_pin_rpi, action_command_turn_off, dir_temp_file

is_on_heater = dir_temp_file + '/is_on_heater'

print "###########################\n"
print "# SET_ACTIVATED_HEATER.py #\n"
print "###########################\n"


writeValueToFile(activated_file,sys.argv[1])
print "Write value %s to %s \n" %(sys.argv[1],activated_file)
if sys.argv[1]=='False' or sys.argv[1]=='false' :
	print "Turn off heater \n" 
	subprocess.call(action_command_turn_off, shell=True)
	print "Write False to the %s\n" %is_on_heater
	writeValueToFile(is_on_heater,'False')
print"\n"
print"###END OF SET_ACTIVATED_HEATER.py###"
print"\n\n"