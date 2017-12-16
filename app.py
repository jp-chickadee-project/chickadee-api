from flask import Flask, request
import flask.logging
from flask.json import JSONEncoder

from db.database import chickadeeDatabase
from views.birds import birds
from views.visits import visits
from views.feeders import feeders

import json
import logging
import traceback
import datetime
import decimal
from time import strftime

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

def log(logger, request, message):
	timestamp = strftime('[%Y-%b-%d %H:%M:%S]')
	logger.info('%s %s %s %s %s %s',
		timestamp,
		request.remote_addr,
		request.method,
		request.scheme,
		request.full_path,
		message)

app = Flask(__name__)

@app.after_request
def after_request(response):
	if response.status_code != 500:
		log(logger, request, response.status)
	return response

@app.errorhandler(Exception)
def exceptions(e):
	backtrace = "500 INTERNAL SERVER ERROR\n" + traceback.format_exc()
	log(logger, request, backtrace)
	return "Internal Server Error", 500

if __name__ == '__main__':
	app.register_blueprint(birds)
	app.register_blueprint(visits)
	app.register_blueprint(feeders)

	app.json_encoder = CustomJSONEncoder

	logger = logging.getLogger(__name__)
	handler = logging.FileHandler('log')
	handler.setLevel(logging.INFO)
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)

	apiconfig = json.load(open('config', 'r'))
	app.config['MYSQL_DATABASE_USER'] = apiconfig["username"]
	app.config['MYSQL_DATABASE_PASSWORD'] = apiconfig["password"]
	app.config['MYSQL_DB'] = apiconfig["database"]
	app.config['DATABASE'] = chickadeeDatabase(app)

	with app.app_context():
		app.config['DATABASE'].mysql.init_app(app)

	startupTime = strftime('[%Y-%b-%d %H:%M:%S]')
	logger.info('%s Running on http://%s:%s/', 
		startupTime,
		apiconfig["host"],
		apiconfig["port"])

	app.run(apiconfig["host"], apiconfig["port"])