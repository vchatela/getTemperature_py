 #!/usr/bin/python
import time
import os
import glob
import MySQLdb as mdb
import sys
from file_save import *
import subprocess

global login
global password
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

dir_temp_file = '/var/www/files'

refresh_time = 30;
refresh_time_heater = 20;

activated_file = dir_temp_file + '/activated_file'
val_required_temp_file = dir_temp_file + '/val_required_temp_file'
val_remaining_refresh_time_file = dir_temp_file + '/val_remaining_refresh_time_file'
val_remaining_add_db_file = dir_temp_file + '/val_remaining_add_db_file'

wiring_pin_rpi = 29
action_command_turn_on = '/var/www/hcc/radioEmission '+str(wiring_pin_rpi)+' 12325261 1 on'
action_command_turn_off = '/var/www/hcc/radioEmission '+str(wiring_pin_rpi)+' 12325261 1 off'



def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
	return temp_c

def add_temp_to_db(temp):
	try:
			db=mdb.connect('localhost', login, password, 'temperature');
			cur = db.cursor()
			cur.execute("INSERT INTO Temperature VALUES (0, CURRENT_DATE(), (CURRENT_TIME()), %f)" %temp)
			db.commit()

	except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)

	finally:
		if db:
			db.close()

def getValueFromFile(file):
	f = open(file, 'r')
	#print "Opened : %s" %file
	s = f.read()
	f.close()
	#print "Closed : %s \n\n" %file
	return s

def writeValueToFile(file, value):
	f = open(file, 'w')
	#print "Opened : %s value %d " %(file,value)
	f.write(str(value))
	f.close()
	#print "Closed : %s \n\n" %file
	return 0

############################################################
#                   Main Program                           #
############################################################

def main():
	# Get Temperature and store it each 20 minutes
	temp = float(read_temp())
	print "Current temperature : %f" %temp

	remaining_time = float(getValueFromFile(val_remaining_add_db_file))
	if(remaining_time==0):
		add_temp_to_db(temp)
		writeValueToFile(val_remaining_add_db_file,refresh_time)
		print "Updated remaining time DB : %d" %int(refresh_time)
	else:
		writeValueToFile(val_remaining_add_db_file,remaining_time-1)
		print "Updated remaining time DB : %d" %(int(remaining_time)-1)


	remaining_time_heater = float(getValueFromFile(val_remaining_refresh_time_file))
	if(remaining_time_heater==0):
		# Get the activated boolean in file
		s_activated = getValueFromFile(activated_file)
		if s_activated=='true' or s_activated=='True':
			b_activated = True
		else:
			b_activated = False
		print "Activated : %s " %(str(b_activated))
		# If activated check if heater is needed
		if b_activated:
		# Get val_temp_requiered in file
			val_temp_required = float(getValueFromFile(val_required_temp_file))
		# Maybe later use a state variable of the heater
			if temp < val_temp_required:
				#turn on heater
				print "turn on heater"
				subprocess.call(action_command_turn_on, shell=True)
			else:
				#turn off heater
				print "turn off heater"
				subprocess.call(action_command_turn_off, shell=True)
		writeValueToFile(val_remaining_refresh_time_file,refresh_time_heater)
		print "Updated remaining time heater %d " %int(refresh_time_heater)
	else:
		writeValueToFile(val_remaining_refresh_time_file,remaining_time_heater-1)
		print "Updated remaining time heater : %d " %(int(remaining_time_heater)-1)

if __name__ == "__main__":
    main()