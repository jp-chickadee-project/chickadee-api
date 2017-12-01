from flask import Flask, request, abort, jsonify
from flask_mysqldb import MySQL
import json
import datetime
from flask.json import JSONEncoder

client_whitelist = [
	'127.0.0.1',
	'198.110.204.9' #euclid
]

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chickadeesTesting'

with app.app_context():
	mysql.init_app(app)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date) or isinstance(obj, datetime.timedelta) or isinstance(obj, datetime.datetime):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

@app.before_request
def limit_remote_addr():
	if request.remote_addr not in client_whitelist:
		abort(403)

@app.route("/api/birds",methods=['GET', 'POST'])
def birds():
	cur = mysql.connection.cursor()
	if request.method == 'GET':
		cur.execute('''SELECT * FROM birds''')

	data = [dict((cur.description[i][0], value)
		for i, value in enumerate(row)) for row in cur.fetchall()]

	return jsonify(data)


if __name__ == "__main__":
	app.run()

