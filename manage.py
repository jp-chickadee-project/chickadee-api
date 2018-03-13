
from flask_script import Manager
import mysql.connector as sql

import unittest

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

if __name__ == "__main__":
	manager.run()