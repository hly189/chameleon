#! /usr/bin/python


from os 	import popen, system 
from socket	import gethostname
from sys	import argv
from getpass	import getpass
import argparse
import pymysql

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

#---- db login 
def dbLogin(user): 
	dbLoginCommand = '/usr/local/mysql/bin/mysql -u %s -p' % user 
	system(dbLoginCommand)

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
def getMySqlConnection(usr='root', password=''): 
	ipaddress   = "127.0.0.1"
	charset     = "utf8mb4"
	curtype     = pymysql.cursors.DictCursor 
	
	if password == '': 
		password = getpass("Enter root password: ")
	
	sqlCon 	    = pymysql.connect(host=ipaddress, user=usr, password=password, charset=charset, cursorclass=curtype)
	sqlCursor   = sqlCon.cursor()
	return sqlCon, sqlCursor 

#---- get db connection
def createDbUser(user, password):
	sqlConn, sqlCursor = getMySqlConnection()
	createUserQuery = "CREATE USER IF NOT EXISTS '%s'@'localhost' IDENTIFIED BY '%s';"%(user, password)
	try: 
		sqlCursor.execute(createUserQuery)
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
	# Init database
	if args.init: 
		createDbUser(dbChameleonUser, dbChameleonPass)
		userList = listDb()
		
		print("List of users:");
		for user in userList:
		    print(user)
main()


