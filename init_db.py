import mysql.connector as sql

tables={}

tables["feeders"] = (
	"create table feeders ("
		"feederID 			char(4) not null unique,"
		"fullName 			varchar(64) not null,"
		"lastPath			varchar(16),"
		"battery 			int unsigned,"
		"latitude 			decimal(10,7),"
		"longitude 			decimal(10,7),"
		"lastStatus			varchar(64),"
		"lastContact		datetime(0),"

		"primary key(feederID)"
	")"
)
tables["birds"] = (
	"create table birds ("
		"fullTimeStamp 		datetime(0),"
		"logDate 			date, "
		"logTime 			time, "
		"bander 			varchar(64), "
		"capSite 			varchar(64), "
		"bandNum			varchar(64), "
		"rfid 				varchar(16) not null unique, "
		"bandCombo			varchar(16), "
		"retrices			varchar(8), "
		"wingChord 			int unsigned, "
		"tailLen			int unsigned, "
		"birdWeight 		decimal(10,4) unsigned, "
		"HY_AHY				int unsigned, "
		"rightLegTop		varchar(64), "
		"rightLegBottom		varchar(64), "
		"leftLegTop			varchar(64), "
		"leftLegBottom		varchar(64), "
		"longestSec			int unsigned, "
		"billDepth			decimal(5,2) unsigned, "
		"billWid			decimal(5,2) unsigned, "
		"billLen			decimal(5,2) unsigned, "
		"bibLen				decimal(5,2) unsigned, "
		"capLen				decimal(5,2) unsigned, "
		"tarsus				decimal(5,2) unsigned, "
		"bagWeight			decimal(10,4) unsigned, "
		"bagAndBirdWeight	decimal(10,4) unsigned, "
		"tissueSample		varchar(32), "
		"suspectedSex		varchar(16), "
		"netEnter			time, "
		"netExit			time, "
		"released			time, "
		"notes				varchar(256), "
		"weather			varchar(256), "
		"image				blob(300000),"

		"primary key(rfid)"
	")"
)

tables["visits"] = (
	"create table visits ("
		"rfid 				varchar(16) not null,"
		"feederID 			char(4) not null,"
		"visitTimeStamp		datetime(0), "
		"temp				int unsigned, "
		"mass				int unsigned, "

		"foreign key(rfid)"
			"references birds(rfid),"
		"foreign key(feederID)"
			"references feeders(feederID)"
	")"
)

uname = input("Enter username: ")
pswd = input("Enter password: ")
cnx = sql.connect(
	user=uname,
	password=pswd
)

DB_NAME = "chickadeesTest"

try:
	cnx.database = DB_NAME  
except sql.Error as err:
	if err.errno == errorcode.ER_BAD_DB_ERROR:
		try:
			cursor.execute(
				"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
		except mysql.connector.Error as err:
			print("Failed creating database: {}".format(err))
			exit(1)

		cnx.database = DB_NAME
	else:
		print(err)
		exit(1)
cursor = cnx.cursor()


for name in tables:
	print("Creating table: " + name)
	cursor.execute(tables[name])

cursor.close()
cnx.close()
