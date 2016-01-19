#!/usr/bin/python
import os
import sys
import subprocess

from script import activated_file, writeValueToFile, val_required_temp_file,val_remaining_refresh_time_file, turnOffHeater, turnOnHeater, read_temp

# sys.argv[1] = temp   sys.argv[2] = activated
# update temp_file with temp
writeValueToFile(val_required_temp_file,sys.argv[1])
print "Writed to %s value %s \n" %(val_required_temp_file,sys.argv[1]) 
writeValueToFile(val_remaining_refresh_time_file,0)
print "Restart counter of %s at 0 \n" %val_remaining_refresh_time_file
# start : set_activated_heater.py activated
if sys.argv[2].lower()==('false' or 'true'):
	print "Set_activated_heater at %s \n" %sys.argv[2]

	writeValueToFile(activated_file,sys.argv[2])
	print "Write value %s to %s \n" %(sys.argv[2],activated_file)
	if sys.argv[2].lower()=='false' :
		turnOffHeater()
		print "Write False to the %s\n" %is_on_heater
	else : 
		print "Test if need to turn on heater \n"
		temp = float(read_temp())
		# Get val_temp_requiered in file
		val_temp_required = float(getValueFromFile(val_required_temp_file))
		if temp < val_temp_required:
			#turn on heater
			turnOnHeater()
		else:
			#turn off heater
			turnOffHeater()
else:
	print "Error with parameter activated at : %s \n" %sys.argv[2]