#!/usr/bin/python
import MySQLdb as mdb
import sys

try:
	db=mdb.connect('localhost','userdist','123456', 'temperature');
	cur = db.cursor()
	#cur.execute=("CREATE TABLE IF NOT EXISTS temperature (id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, date DATE NOT NULL DEFAULT '0000-00-00', heure TIME NOT NULL DEFAULT '00:00:00', temperature FLOAT)")
	cur.execute("INSERT INTO Temperature VALUES ( 1, CURDATE(), CURTIME(), 15)")
	cur.execute("show grants")

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)

#finally:
#	if db:
#		db.close()
