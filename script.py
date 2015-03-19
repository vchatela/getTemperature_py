 
#!/usr/bin/python
import time
import os
import glob
import MySQLdb

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

db=MySQLdb.connect(host="88.142.52.11",db="temperature", user= "root", passwd="Oybocphideitevifoch0")
db.query=("CREATE TABLE IF NOT EXISTS temperature (id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, date DATE NOT NULL DEFAULT '0000-00-00', heure TIME NOT NULL DEFAULT '00:00:00', temperature FLOAT)")

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

print(read_temp())
db.query('INSERT INTO temperature VALUES ( null, CURDATE(), CURTIME(), ' + "%.2f" % temp_c')')
		 