from flask import Flask
from flask_mysqldb import MySQL
from flask.json import JSONEncoder

import json
import datetime
import decimal

app = Flask(__name__)
mysql = MySQL()

class CustomJSONEncoder(JSONEncoder):
	def default(self, obj):
		try:
			if isinstance(obj, datetime.date) or isinstance(obj, datetime.timedelta) or isinstance(obj, datetime.datetime):
				return str(obj)
			if isinstance(obj, decimal.Decimal):
				return float(obj)
			iterable = iter(obj)
		except TypeError:
			pass
		else:
			return list(iterable)
		return JSONEncoder.default(self, obj)

def query(aQuery):
	cur = mysql.connection.cursor()
	cur.execute(aQuery)

	data = [dict((cur.description[i][0], value)
		for i, value in enumerate(row)) for row in cur.fetchall()]

	if len(data) == 1:
		data = data[0]
	return data