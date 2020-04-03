#! /usr/bin/env python3


from os		import popen, system
from sys	import argv
import argparse
import pymysql
import myloginpath

#-------------------------------------------------------------
# Global Varibles 
#-------------------------------------------------------------
chamelenonDb = 'chameleon'


#-------------------------------------------------------------
# Functions 
#-------------------------------------------------------------
#----- Get db connection
def getMySqlConnection(usr='root'):
	global chamelenonDb
	
	ipaddress   = "127.0.0.1"
	charset     = "utf8mb4"
	curtype     = pymysql.cursors.DictCursor

	conf = myloginpath.parse(usr)
	sqlCon		= pymysql.connect(**conf, host=ipaddress, charset=charset, cursorclass=curtype)
	sqlCursor   = sqlCon.cursor()
	return sqlCon, sqlCursor


#----- Load Data into database
def loadCityData(fileName): 
	global chamelenonDb	
	sqlConn, sqlCursor = getMySqlConnection(chamelenonDb) 
		
	f = open(fileName, 'r')
	
	for item in f: 
		listData = item.strip().split(',')
		sqlQuery = "INSERT INTO %s.CITYTBL(CITYID, CITY_NAME, STATE, COUNTRY) VALUES (%s, '%s', '%s', '%s');" %(chamelenonDb, listData[0], listData[1], listData[2], listData[3])
		try: 
			sqlCursor.execute(sqlQuery)
			sqlConn.commit()
		except Exception as ex: 
			print("ERROR: Query PROBLEM: %s" % sqlQuery)
			exit(1)
	sqlCursor.close()
	sqlConn.close()
	f.close()
