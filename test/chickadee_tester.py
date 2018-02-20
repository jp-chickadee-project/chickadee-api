import unittest
import logging

from app import app, CustomJSONEncoder
from db.database import chickadeeDatabase

from views.birds import birds
from views.visits import visits
from views.feeders import feeders
from views.users import users


#This class is subclassed by the other testing since the process 
#for setting up the flaskapp is identical across test cases


TEST_DB = 'chickadeesTesting'

class ChickadeeTester(unittest.TestCase):
	def setUp(self):
		app.register_blueprint(birds)
		app.register_blueprint(visits)
		app.register_blueprint(feeders)
		app.register_blueprint(users)

		app.json_encoder = CustomJSONEncoder

		logger = logging.getLogger(__name__)
		handler = logging.FileHandler('log.test')
		handler.setLevel(logging.INFO)
		logger.addHandler(handler)
		logger.setLevel(logging.INFO)

		app.config["LOGGER"] = logger
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False

		app.config['MYSQL_DATABASE_USER'] = ""
		app.config['MYSQL_DATABASE_PASSWORD'] = ""
		app.config['MYSQL_DB'] = TEST_DB
		app.config['DATABASE'] = chickadeeDatabase()       

		with app.app_context():
			app.config['DATABASE'].mysql.init_app(app)

		self.app = app.test_client()
		self.assertEqual(app.debug, False)

	def tearDown(self):
		pass
 