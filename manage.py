
from flask_script import Manager
import mysql.connector as sql

import unittest
import os
import sys
import json
import time
import datetime
import zipfile
from chickadee_api import create_app

manager = Manager(create_app)

@manager.command
def test():
	tests = unittest.TestLoader().discover('test', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		return 0
	return 1

@manager.command
def createdb(username="", password="", dbname="chickadees"):
	cnx = sql.connect(
		user=username,
		password=password
	)

	cursor = cnx.cursor(buffered=True)
	cnx.get_warnings=True

	cursor.execute("CREATE DATABASE IF NOT EXISTS " + dbname)
	cursor.execute("USE " + dbname)

	with open('chickadee_api/db/schema.sql', 'r') as f:
		schema = f.read()

	commands = schema.split(';')

	for cmd in commands:
		try:
			cursor.execute(cmd)
		except:
			print("Error parsing command: " + cmd)
			exit()

	cursor.close()
	cnx.commit()
	cnx.close()

	print("Database created")

@manager.command
def loadvisits(visitzip="", db="", username="", password=""):
	if not visitzip:
		print("Visit zipfile location not entered, exiting")
		return

	cnx = sql.connect(
		user=username,
		password=password,
		database=db
	)
	cursor = cnx.cursor(buffered=True)
	cnx.get_warnings=True

	visitzip = zipfile.ZipFile(visitzip)

	for f in visitzip.infolist():
		feederID = f.filename.split("/")[-1][:4]
		if feederID == "RFID":
			continue

		print("Loading file:  " + f.filename)
		for line in visitzip.open(f).readlines()[2:]:
			line = line.decode("utf-8").rstrip("\r\n").split(" ")
			rfid = line[0]

			date = str(line[1][:-2]) + "20" + str(line[1][-2:])
			timestamp = date + " " + line[2][:-1]
			timestamp = time.mktime(datetime.datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S").timetuple())

			cursor.execute("SELECT bandCombo FROM birds WHERE rfid = '{0}';".format(rfid))
			bandCombo = cursor.fetchone()[0]

			command = (
				"INSERT INTO visits (rfid, visitTimestamp, feederID, bandCombo, temperature, mass) "
				"VALUES ('{0}', '{1}', '{2}', '{3}', 0, 0);".format(rfid, timestamp, feederID, bandCombo))
			cursor.execute(command)

		warnings = cursor.fetchwarnings()
		if warnings: print(warnings)

		print("Completed file: " + f.filename)
	cnx.commit()
	print("Visits loaded")

if __name__ == "__main__":
	manager.run()