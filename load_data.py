import mysql.connector as sql
import csv
import os
from itertools import islice

translation = {
	"CARP":["Carpenter", "46.55446", "-87.42682"],
	"JPHQ":["Headquarters", "46.556522", "-87.427372"],
	"RILE":["Riley", "46.554838", "-87.430591"],
	"CLIF":["Cliff", "46.5523", "-87.4243"],
	"SHRM":["Sherman", "46.55102", "-87.42213"],
	"SPRO":["Sproul", "46.552196", "-87.431967"],
	"HMST":["Homestead", "46.55368", "-87.42843"],
	"WEST":["WestEnd", "46.554580", "-87.433253"],
}

uname = input("Enter username: ")
pswd = input("Enter password: ")
cnx = sql.connect(
	user=uname,
	database='chickadeesTest',
	password=pswd
)


cursor = cnx.cursor()

#TODO: combine date and time into datetime variables
load_file = (
	"load data local infile %s "
	"into table visits fields terminated by ' ' "
	"ignore 2 rows "
	"(rfid, @varDate, @varTime) "
	"set visitDate = DATE_FORMAT(STR_TO_DATE(@tempdate, '%m/%d/%Y'), '%Y-%m-%d'), "
	"feederID = %s"
)

load_birds = (
	"load data local infile '/home/michael/Documents/birdproject/chickadee-server/rfid_data.csv"
	"into table birds fields terminated by ',' "
	"ignore 1 rows "
	""
)

load_feeders = (

)

#for f in os.listdir("olddata"):
	#cursor.execute(load_file, (os.getcwd() + "/olddata/" + f, f[:4]))
	#print(f + " completed")

#cnx.commit()
cnx.close()
