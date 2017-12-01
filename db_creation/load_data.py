import mysql.connector as sql
import csv
import os
from itertools import islice
from pprint import *

rfid_data_path = os.getcwd() + "/rfid_data.csv"
feeder_data_path = os.getcwd() + "/feeder_data.csv"
visit_data_path = os.getcwd() + "/visit_data/"

uname = input("Enter username: ")
pswd = input("Enter password: ")
cnx = sql.connect(
	user=uname,
	database='chickadeesTesting',
	password=pswd
)


cursor = cnx.cursor(buffered=True)
cnx.get_warnings=True
load_file = (
	"load data local infile %s "
	"into table visits fields terminated by ' ' "
	"ignore 2 rows "
	"(rfid, @varDate, @varTime) "
	"set "
		"visitTimestamp = UNIX_TIMESTAMP(STR_TO_DATE(CONCAT_WS(' ',@varDate,@varTime), '%m/%d/%Y %T')), "
		"feederID = %s,"
		"temperature = 0,"
		"mass = 0"
)

load_birds = (
	"load data local infile '" + rfid_data_path + "' "
	"into table birds fields terminated by ',' "
	"optionally enclosed by '\"' " 
	"lines terminated by '\r\n' "
	"ignore 1 lines "
	"(@varLogTimestamp, "
		"@varDate, "
		"@varTime, "
		"species, "
		"captureSite, "
		"bandNumber, "
		"rfid, "
		"rightLegTop, "
		"rightLegBottom, "
		"leftLegTop, "
		"leftLegBottom, "
		"tailLength, "
		"wingChord, "
		"longestSecondary, "
		"billDepth, "
		"billWidth, "
		"billLength, "
		"bibLength, "
		"capLength, "
		"tarsus, "
		"bagWeight, "
		"bagAndBirdWeight, "
		"birdWeight, "
		"tissueSample, "
		"suspectedSex, "
		"@varEnter, "
		"@varExit, "
		"@varReleased, "
		"notes, "
		"weather, "
		"banders "
	") "
	"set "
		"logTimestamp = UNIX_TIMESTAMP(STR_TO_DATE(@varLogTimestamp, '%m/%d/%Y %T')), "
		"captureTimestamp = UNIX_TIMESTAMP(STR_TO_DATE(CONCAT(@varDate, ' ', @varTime), '%m/%d/%Y %T')), "
		"netEnter = UNIX_TIMESTAMP(STR_TO_DATE(CONCAT(@varDate, ' ', TIME_FORMAT(STR_TO_DATE(@varEnter, '%r'), '%T')), '%m/%d/%Y %T')), "
		"netExit = UNIX_TIMESTAMP(STR_TO_DATE(CONCAT(@varDate, ' ', TIME_FORMAT(STR_TO_DATE(@varExit, '%r'), '%T')), '%m/%d/%Y %T')), "
		"released = UNIX_TIMESTAMP(STR_TO_DATE(CONCAT(@varDate, ' ', TIME_FORMAT(STR_TO_DATE(@varReleased, '%r'), '%T')), '%m/%d/%Y %T')) "
)

load_feeders = (
	"load data local infile '" + feeder_data_path + "' "
	"into table feeders fields terminated by ',' "
	"ignore 1 rows "
	"(feederID,fullName,lastPath,battery,latitude,longitude,lastStatus,lastContact) "
)

cursor.execute(load_birds)
print("Birds loaded")
cnx.commit()

cursor.execute(load_feeders)
print("Feeders loaded")
cnx.commit()

for f in os.listdir("visit_data"):
	cursor.execute(load_file, (visit_data_path + f, f[:4]))
	pprint(cursor.fetchwarnings())

	print(f + " completed")
print("Visits Loaded")

cursor.close()
cnx.commit()
cnx.close()
