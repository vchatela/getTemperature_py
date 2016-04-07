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
nb_device = len(glob.glob(base_dir + '28*'))

dir_temp_file = '/var/www/files'

refresh_time = 30;
refresh_time_heater = 10;

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
			db=mdb.connect('localhost', login, password, 'temperature')
			cur = db.cursor()
			value = getValueFromFile(activated_file)
			cur.execute("INSERT INTO Temperature VALUES (0, CURRENT_DATE(), (CURRENT_TIME()), %f, %s)" %(temp,value))
			db.commit()

	except mdb.Error, e:
			print "Error %d: %s \n" % (e.args[0],e.args[1])
			sys.exit(1)

	finally:
		if db:
			db.close()

def getValueFromFile(file):
	f = open(file, 'r')
	s = f.read()
	f.close()
	return s

def writeValueToFile(file, value):
	f = open(file, 'w')
	f.write(str(value))
	f.close()
	return 0

def turnOnHeater():
	print "turn on heater \n"
	subprocess.call(action_command_turn_on, shell=True)

def turnOffHeater():
	print "turn off heater \n"
	subprocess.call(action_command_turn_off, shell=True)

############################################################
#                   Main Program                           #
############################################################

def main():
	if nb_device>0:
		device_folder = glob.glob(base_dir + '28*')[0]
		device_file = device_folder + '/w1_slave'
		#If the heater it should not be activated - turn off (activated_heater off)
		if getValueFromFile(activated_file).lower()=="false":
			turnOffHeater()
		# Get Temperature and store it each 20 minutes
		temp = float(read_temp())
		print "Current temperature : %f \n" %temp

		remaining_time = float(getValueFromFile(val_remaining_add_db_file))
		if(remaining_time==0):
			add_temp_to_db(temp)
			writeValueToFile(val_remaining_add_db_file,refresh_time)
			print "Updated remaining time DB : %d \n" %int(refresh_time)
		else:
			writeValueToFile(val_remaining_add_db_file,remaining_time-1)
			print "Updated remaining time DB : %d \n" %(int(remaining_time)-1)

		remaining_time_heater = float(getValueFromFile(val_remaining_refresh_time_file))
		if(remaining_time_heater==0):
			# Get the activated boolean in file
			s_activated = getValueFromFile(activated_file)
			if s_activated.lower()=='true':
				b_activated = True
			else:
				b_activated = False
			print "Activated : %s \n" %(str(b_activated))
			# If activated check if heater is needed
			if b_activated:
			# Get val_temp_requiered in file
				val_temp_required = float(getValueFromFile(val_required_temp_file))
				if temp < val_temp_required:
					#turn on heater
					turnOnHeater()
				else:
					#turn off heater
					turnOffHeater()
			writeValueToFile(val_remaining_refresh_time_file,refresh_time_heater)
			print "Updated remaining time heater %d \n" %int(refresh_time_heater)
		else:
			writeValueToFile(val_remaining_refresh_time_file,remaining_time_heater-1)
			print "Updated remaining time heater : %d \n" %(int(remaining_time_heater)-1)

if __name__ == "__main__":
	main()