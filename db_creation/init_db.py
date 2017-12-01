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
		"lastContact		bigint unsigned,"

		"primary key(feederID)"
	")"
)
tables["birds"] = (
	"create table birds ("
		"logTimestamp		bigint unsigned,"
		"captureTimestamp	bigint unsigned, "
		"species 			varchar(8), "
		"captureSite		varchar(64), "
		"bandNumber			varchar(64), "
		"rfid 				varchar(16) not null unique, "
		"rightLegTop		varchar(64), "
		"rightLegBottom		varchar(64), "
		"leftLegTop			varchar(64), "
		"leftLegBottom		varchar(64), "
		"tailLength			int unsigned, "
		"wingChord 			int unsigned, "
		"longestSecondary	int unsigned, "
		"billDepth			decimal(5,2) unsigned, "
		"billWidth			decimal(5,2) unsigned, "
		"billLength			decimal(5,2) unsigned, "
		"bibLength			decimal(5,2) unsigned, "
		"capLength			decimal(5,2) unsigned, "
		"tarsus				decimal(5,2) unsigned, "
		"bagWeight			decimal(10,4) unsigned, "
		"bagAndBirdWeight	decimal(10,4) unsigned, "
		"birdWeight 		decimal(10,4) unsigned, "
		"tissueSample		varchar(32), "
		"suspectedSex		varchar(16), "
		"netEnter			bigint unsigned, "
		"netExit			bigint unsigned, "
		"released			bigint unsigned, "
		"notes				varchar(256), "
		"weather			varchar(256), "
		"banders 			varchar(64), "
		"image				blob(300000),"

		"primary key(rfid)"
	")"
)

tables["visits"] = (
	"create table visits ("
		"rfid 				varchar(16) not null,"
		"feederID 			char(4) not null,"
		"visitTimestamp		bigint unsigned, "
		"temperature		int unsigned, "
		"mass				int unsigned, "

		"foreign key(rfid) "
			"references birds(rfid), "
		"foreign key(feederID) "
			"references feeders(feederID)"
	")"
)

uname = input("Enter username: ")
pswd = input("Enter password: ")
cnx = sql.connect(
	user=uname,
	password=pswd
)

cnx.database = "chickadeesTesting"
cursor = cnx.cursor()


for name in tables:
	print("Creating table: " + name)
	cursor.execute(tables[name])

cursor.close()
cnx.close()
