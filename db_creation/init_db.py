import mysql.connector as sql

tables={}

tables["feeders"] = (
	"create table feeders ("
		"id 				char(4) not null unique,"
		"fullName 			varchar(64) not null,"
		"lastPath			varchar(16),"
		"battery 			int unsigned,"
		"latitude 			decimal(10,7),"
		"longitude 			decimal(10,7),"
		"lastStatus			varchar(64),"
		"lastContactTimestamp bigint unsigned,"

		"primary key(id)"
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
		"legRightTop		varchar(64), "
		"legRightBottom		varchar(64), "
		"legLeftTop			varchar(64), "
		"legLeftBottom		varchar(64), "
		"tailLength			int unsigned, "
		"wingChordLength	int unsigned, "
		"longestSecondary	int unsigned, "
		"billDepth			decimal(5,2) unsigned, "
		"billWidth			decimal(5,2) unsigned, "
		"billLength			decimal(5,2) unsigned, "
		"bibWidth			decimal(5,2) unsigned, "
		"capLength			decimal(5,2) unsigned, "
		"tarsusLength		decimal(5,2) unsigned, "
		"bagWeight			decimal(10,4) unsigned, "
		"bagAndBirdWeight	decimal(10,4) unsigned, "
		"birdWeight 		decimal(10,4) unsigned, "
		"tissueSample		varchar(32), "
		"suspectedSex		varchar(16), "
		"netEnterTimestamp	bigint unsigned, "
		"netExitTimestamp	bigint unsigned, "
		"releasedTimestamp	bigint unsigned, "
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
			"references feeders(id)"
	")"
)

config = json.load(open('../config', 'r'))

cnx = sql.connect(
	user=config["username"],
	password=config["password"],
	database=config["database"]
)

cursor = cnx.cursor()

for name in tables:
	print("Creating table: " + name)
	cursor.execute(tables[name])

cursor.close()
cnx.close()
