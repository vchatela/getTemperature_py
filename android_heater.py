#!/usr/bin/python
import os
import sys
import subprocess

from script import activated_file, writeValueToFile, val_required_temp_file,val_remaining_refresh_time_file

print "#####################\n"
print "# ANDROID_HEATER.py #\n"
print "#####################\n"

# sys.argv[1] = temp   sys.argv[2] = activated
# update temp_file with temp
writeValueToFile(val_required_temp_file,sys.argv[1])
print "Writed to %s value %s \n" %(val_required_temp_file,sys.argv[1]) 
writeValueToFile(val_remaining_refresh_time_file,0)
print "Restart counter of %s at 0 \n" %val_remaining_refresh_time_file
# start : set_activated_heater.py activated
if sys.argv[2]=='False' or sys.argv[2]=='false' or sys.argv[2]=='True' or sys.argv[2]=='true' :
	subprocess.call("python set_activated_heater.py %s" %sys.argv[2], shell=True)
	print "Set_activated_heater at %s \n" %sys.argv[2]
else:
	print "Error with parameter activated at : %s \n" %sys.argv[2]
print"\n"
print"###END OF ANDROID_HEATER.py###"
print"\n\n"