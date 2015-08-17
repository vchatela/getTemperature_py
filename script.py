 #!/usr/bin/python
import time
import os
import glob
import MySQLdb as mdb
import sys
from file_save import *

global login
global password
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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

def add_temp(temp):
	try:
        	db=mdb.connect('localhost', login, password, 'temperature');
	        cur = db.cursor()
        	#print(db)
	        #print(cur)
	        cur.execute("INSERT INTO Temperature VALUES (0, CURRENT_DATE(), (CURRENT_TIME()), %f)" %temp)
       		db.commit()
#      		result = cur.fetchall()
#      		print result

	except mdb.Error, e:
        	print "Error %d: %s" % (e.args[0],e.args[1])
	        sys.exit(1)

	finally:
		if db:
			db.close()


#Debut du codage !
temp = float(read_temp())
add_temp(temp)
#if not(temp > 0 and temp<35):
#	add_temp(temp)
print(temp)

