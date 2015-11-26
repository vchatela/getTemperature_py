#!/usr/bin/python
import os
import sys
import subprocess

from script import activated_file, writeValueToFile, val_required_temp_file

# sys.argv[1] = temp   sys.argv[2] = activated
# update temp_file with temp
writeValueToFile(val_required_temp_file,sys.argv[1])
print "Writed to %s value %s" %(val_required_temp_file,sys.argv[1]) 
# start : set_activated_heater.py activated
if sys.argv[2]=='False' or sys.argv[2]=='false' or sys.argv[2]=='True' or sys.argv[2]=='true' :
	subprocess.call("python set_activated_heater.py %s" %sys.argv[2], shell=True)
	print "Set_activated_heater at %s " %sys.argv[2]
else:
	print "Error with parameter activated at : %s" %sys.argv[2]