from flask import Flask, jsonify
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
	mysql.connection.commit()

	data = [dict((cur.description[i][0], value)
		for i, value in enumerate(row)) for row in cur.fetchall()]

	if len(data) == 1:
		data = data[0]
	return jsonify(data)

def queryVisitRange(start, end, field="", key=""):
	keyCondition = ""
	if key:
		keyCondition = "visits." + field + " = '" + key + "' AND "
		
	return query(
		"SELECT * FROM " + "visits" + 
			" WHERE " + keyCondition + 
			"visits.visitTimestamp BETWEEN " + start + " AND " + end + ";")

def queryRow(table, field, key):
	return query("SELECT * FROM " + table + " WHERE " + field + " = '" + key + "';")

def queryAddRow(table, form):
	fields = ", ".join([key for key in form.keys()])
	values = "', '".join([val for val in form.values()])

	return query("INSERT INTO " + table + " (" + fields + ") VALUES ('" + values + "');")

def queryTable(table):
	return query("SELECT * FROM " + table)

def queryDeleteOne(table, field, key):
	return query("DELETE FROM "+ table + " WHERE "+ field + " = " + feederID + ";")

