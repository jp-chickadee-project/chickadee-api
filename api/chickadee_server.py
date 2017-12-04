from flask import Flask, request, abort, jsonify
from flask.json import JSONEncoder
from flask_mysqldb import MySQL

import json
import datetime
import decimal
import sys

mysql = MySQL()
app = Flask(__name__)

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
	return jsonify(data)

"""
@app.before_request
def limit_remote_addr():
	if request.remote_addr not in client_whitelist:
		abort(403)
"""

@app.route("/api/birds/<rfid>", methods=['GET'])
def birdsByID(rfid):
	start = request.args.get("start")
	end = request.args.get("end")

	if start and end:
		return query("SELECT * FROM visits "
					"WHERE  visits.rfid = '" + rfid + "' " 
					"AND visits.visitTimestamp BETWEEN " + start + " AND " + end + ";")

	return query("SELECT * FROM birds WHERE rfid = '" + rfid + "' ;")

@app.route("/api/birds/", methods=['GET', 'POST'])
def birds():
	if request.method == 'GET':
		rfid = request.args.get("rfid")
		if rfid:
			return birdsByID(rfid)
		return query("SELECT * FROM birds")

@app.route("/api/feeders/<feederID>", methods=['GET'])
def feedersByID(feederID):
	start = request.args.get("start")
	end = request.args.get("end")
	if start and end:
		return query("SELECT * FROM visits "
					"WHERE  visits.feederID = '" + feederID + "' " 
					"AND visits.visitTimestamp BETWEEN " + start + " AND " + end + ";")
	else:
		return query("SELECT * FROM feeders WHERE id = '" + feederID + "' ;")

@app.route("/api/feeders", methods=['GET', 'POST'])
def feeders():
	if request.method == 'GET':
		feederID = request.args.get("feederID")
		if feederID:
			return feedersByID(feederID)
		return query("SELECT * FROM feeders")

@app.route("/api/visits", methods=['GET', 'POST'])
def visits():
	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")
		return query("SELECT * FROM visits "
					"WHERE visits.visitTimestamp BETWEEN " + start + " AND " + end + ";")



if __name__ == "__main__":
	apiconfig = json.load(open('../config', 'r'))
	
	app.json_encoder = CustomJSONEncoder

	# MySQL configurations
	app.config['MYSQL_DATABASE_USER'] = apiconfig["username"]
	app.config['MYSQL_DATABASE_PASSWORD'] = apiconfig["password"]
	app.config['MYSQL_DB'] = apiconfig["database"]

	with app.app_context():
		mysql.init_app(app)

	app.run(host=apiconfig["host"], port=apiconfig["port"])