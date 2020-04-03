#! /usr/bin/env python3

from os 	import popen, system
from socket	import gethostname
from sys	import argv
from getpass	import getpass
import argparse
import pymysql
import myloginpath

#-------------------------------------------------------------
# Functions
#-------------------------------------------------------------
#---- get agrgs
def get_args():

	parser = argparse.ArgumentParser()
	parser.add_argument('-start', action='store_true')
	parser.add_argument('-stop', action='store_true')
	parser.add_argument('-restart', action='store_true')
	parser.add_argument('-init', action='store_true')
	parser.add_argument('-help', action='store_true')
	parser.add_argument('-login', nargs='+')
	parser.add_argument('-e', nargs='+')
	parser.add_argument('-file', nargs='+')

	args = parser.parse_args()
	return args

#---- db help
def dbHelp():
	print("Usage %s -help, -start, -stop, -init, -restart, -login" % argv[0])
	print("-help: Usage")
	print("-start: Start Database")
	print("-stop: Stop Database")
	print("-restart: Restart Database")
	print("-init: initialize user and password for chameleon")
	print("-login <user> - login to user")
	print('-e "<sql query>" - execute query')
	print('-file <sql file> - execute file sql')

#---- Set login without password
def setlogin(user):
	print("Set login for user: %s" % user)
	dbLoginCommand = '/usr/local/mysql/bin/mysql_config_editor set --login-path=%s --user=%s --password' % (user, user)
	system(dbLoginCommand)


#---- db login
def dbLogin(user):
	dbLoginCommand = '/usr/local/mysql/bin/mysql --login-path=%s' % user
	system(dbLoginCommand)

#---- db execute
def dbExecuteQuery(user, sqlQuery):
	dbCommand = '/usr/local/mysql/bin/mysql --login-path=%s -e "%s"' % (user, sqlQuery)
	system(dbCommand)

#---- db file execute
def dbExecuteFile(user, sqlFile):
	dbCommand = '/usr/local/mysql/bin/mysql --login-path=%s < %s' % (user, sqlFile)
	system(dbCommand)

#---- db service
def dbService(command):
	dbCommand = "sudo /usr/local/mysql/support-files/mysql.server %s" % command
	popen(dbCommand).read()

	checkRunning = popen("ps -ef | grep mysql | grep -v grep > /dev/null 2>&1; echo $?").read().strip()

	if int(checkRunning) == 0:
		print("MySQL started successfully")
	else:
		if command == 'stop' and int(checkRunning) != 0:
			print("MySQL stopped successfully")
			return
		print("Falied to Start")

#---- get db connection
def getMySqlConnection(usr='root'):
	ipaddress   = "127.0.0.1"
	charset     = "utf8mb4"
	curtype     = pymysql.cursors.DictCursor

	conf = myloginpath.parse(usr)
	sqlCon 	    = pymysql.connect(**conf, host=ipaddress, charset=charset, cursorclass=curtype)
	sqlCursor   = sqlCon.cursor()
	return sqlCon, sqlCursor

#---- get db connection
def createDbUser(user, password):
	sqlConn, sqlCursor = getMySqlConnection()
	sqlQueryList = ["CREATE USER IF NOT EXISTS '%s'@'localhost' IDENTIFIED BY '%s';"%(user, password),
                    "GRANT ALL PRIVILEGES ON * . * TO '%s'@'localhost';" %(user)]
	
	for sqlQuery in sqlQueryList:
		try:
			sqlCursor.execute(sqlQuery)
		except Exception as ex:
			print("ERROR: Falied to create User: %s" % user)
			exit()


#---- show
def listDb():
	sqlConn, sqlCursor = getMySqlConnection()
	sqlQuery = "select host, user from mysql.user;"

	try:
		sqlCursor.execute(sqlQuery)
	except Exception as ex:
		print("ERROR: Falied to fetch data")
		exit()
	userList = sqlCursor.fetchall()
	sqlCursor.close()
	sqlConn.close()

	return userList

def main():
	args = get_args()

	dbChameleonUser = 'chameleon'
	dbChameleonPass = 'chameleon!23'


	# Print out Usage
	if args.help:
		dbHelp()

	# Start MySQL
	if args.start:
		dbService("start")

	# Stop MySQL
	if args.stop:
		dbService("stop")

	# Restart MySQL
	if args.restart:
		dbService("restart")

	# Login MySQL
	if args.login:
		dbLogin(args.login[0])
	
	# Execute query in MySQL
	if args.e:
		dbExecuteQuery(dbChameleonUser, args.e[0])
	
	# Execute file SQL
	if args.file:
		dbExecuteFile(dbChameleonUser, args.file[0])
	
	# Init database
	if args.init:
		# Set login-path for root
		setlogin('root')
		createDbUser(dbChameleonUser, dbChameleonPass)
		# Set login-path for chameleon
		print("Password for chameleon is %s" % dbChameleonPass)
		setlogin(dbChameleonUser)
		userList = listDb()

		print("List of users:");
		for user in userList:
		    print(user)
main()
