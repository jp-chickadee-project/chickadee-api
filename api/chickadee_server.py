from shared_funcs import *
from feeders_api import feeders
from birds_api import birds
from visits_api import visits

import json

"""
@app.before_request
def limit_remote_addr():
	if request.remote_addr not in client_whitelist:
		abort(403)
"""

if __name__ == "__main__":
	app.register_blueprint(birds)
	app.register_blueprint(visits)
	app.register_blueprint(feeders)

	app.json_encoder = CustomJSONEncoder

	apiconfig = json.load(open('../config', 'r'))
	app.config['MYSQL_DATABASE_USER'] = apiconfig["username"]
	app.config['MYSQL_DATABASE_PASSWORD'] = apiconfig["password"]
	app.config['MYSQL_DB'] = apiconfig["database"]

	with app.app_context():
		mysql.init_app(app)

	app.run(apiconfig["host"], apiconfig["port"])