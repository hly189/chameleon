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
		sqlQuery = """INSERT INTO {DBNAME}.CITYTBL(CITYID, CITY_NAME, STATE, COUNTRY, COUNTY, LATITUDE, LONGTITUDE) VALUES ({CITYID}, "{CITY_NAME}", "{STATE}", "{COUNTRY}", "{COUNTY}", {LATITUDE}, {LONGTITUDE});""" .format(DBNAME=chamelenonDb, CITYID=listData[0], CITY_NAME=listData[1], STATE=listData[2], COUNTRY=listData[3], COUNTY=listData[4], LATITUDE=listData[5], LONGTITUDE=listData[6])
		try: 
			sqlCursor.execute(sqlQuery)
			sqlConn.commit()
		except Exception as ex: 
			print("ERROR: Query PROBLEM: %s" % sqlQuery)
			exit(1)
	sqlCursor.close()
	sqlConn.close()
	f.close()
