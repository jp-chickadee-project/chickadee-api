from flask import Flask, request, abort, jsonify
from flask_mysqldb import MySQL
import json
import datetime
from flask.json import JSONEncoder
import decimal

client_whitelist = [
	'127.0.0.1',
	'198.110.204.9' #euclid
]

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = input("Enter MySQL username: ")
app.config['MYSQL_DATABASE_PASSWORD'] = input("Enter MySQL password: ")
app.config['MYSQL_DB'] = input("Enter MySQL database: ")

with app.app_context():
	mysql.init_app(app)

class CustomJSONEncoder(JSONEncoder):
	def default(self, obj):
		try:
			if isinstance(obj, datetime.date) or isinstance(obj, datetime.timedelta) or isinstance(obj, datetime.datetime):
				return str(obj)
			if isinstance(obj, decimal.Decimal):
				return str(obj)
			iterable = iter(obj)
		except TypeError:
			pass
		else:
			return list(iterable)
		return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

def query(aQuery):
	cur = mysql.connection.cursor()
	cur.execute(aQuery)

	data = [dict((cur.description[i][0], value)
		for i, value in enumerate(row)) for row in cur.fetchall()]

	return jsonify(data)



"""
@app.before_request
def limit_remote_addr():
	if request.remote_addr not in client_whitelist:
		abort(403)
"""



@app.route("/api/birds/<rfid>", methods=['GET'])
def birdsByID(rfid):
	return query("SELECT * FROM birds WHERE rfid = '" + rfid + "' ;")

@app.route("/api/birds/", methods=['GET', 'POST'])
def birds():
	if request.method == 'GET':
		rfid = request.args.get("rfid")
		if rfid:
			return birdsByID(rfid)
		return query('''SELECT * FROM birds''')





@app.route("/api/feeders/<feederID>", methods=['GET'])
def feedersByID(feederID):
	return query("SELECT * FROM feeders WHERE feederID = '" + feederID + "' ;")

@app.route("/api/feeders", methods=['GET', 'POST'])
def feeders():
	if request.method == 'GET':
		return query('''SELECT * FROM feeders''')



if __name__ == "__main__":
	host = input("Enter host to run on: ")
	port = input("Enter port: ")
	app.run(host="localhost", port=8155)

