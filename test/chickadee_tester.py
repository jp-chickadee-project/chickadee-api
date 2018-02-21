import unittest

from chickadee_api import create_app

app = create_app(config_name="testing")

class ChickadeeTester(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.assertEqual(app.debug, False)
