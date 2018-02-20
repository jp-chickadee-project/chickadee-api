import unittest
import json

from pprint import pprint
from chickadee_tester import ChickadeeTester

class TestFeeders(ChickadeeTester):
	def setUp(self):
		super(TestFeeders, self).setUp()

		self.testFeeder = {
			"battery": 98, 
			"fullName": "feederForTesting", 
			"id": "TEST", 
			"lastContact": 12, 
			"lastPath": "", 
			"lastStatus": "", 
			"latitude": 46, 
			"longitude": -87
		}
		
	def tearDown(self):
		self.app.delete('/api/feeders/TESTFEEDER')

	def testGetAll(self):
		response = self.app.get('/api/feeders/')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data)
		response = json.loads(response.data.decode())

		self.assertTrue(response[0]['id'])
		self.assertTrue(response[0]['fullName'])

	def testGetOne(self):
		response = self.app.get('/api/feeders/CARP')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(response['id'], "CARP")

		response = self.app.get('/api/feeders/nonsense')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data.decode(), "404 - Specified feeder does not exist")

	def testPost(self):
		response = self.app.post('/api/feeders/', data=self.testFeeder)

		self.assertEqual(response.status_code, 201)
		self.assertTrue(response.data)
		response = json.loads(response.data.decode())

		for key in self.testFeeder:
			self.assertEqual(self.testFeeder[key], response[key])

		invalidFeeder = self.testFeeder.copy()
		invalidFeeder["id"] = ""
		response = self.app.post('/api/feeders/', data=invalidFeeder)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.decode(), 'feederID not supplied')

	def testPut(self):
		self.app.post('/api/feeders/', data=self.testFeeder)

		temp = self.testFeeder.copy()
		temp["battery"] = 20
		temp["lastContact"] = 100
		response = self.app.put('/api/feeders/TEST', data=temp)

		self.assertEqual(response.status_code, 201)
		response = json.loads(response.data.decode())

		for key in temp:
			self.assertEqual(temp[key], response[key])

		temp["id"] = ""
		response = self.app.post('/api/feeders/', data=temp)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.decode(), 'feederID not supplied')

	def testDelete(self):
		self.app.post('/api/feeders/', data=self.testFeeder)

		response = self.app.delete('/api/feeders/TEST')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.data.decode(), '')

		response = self.app.get('/api/feeders/TEST')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data.decode(), "404 - Specified feeder does not exist")

if __name__ == "__main__":
	unittest.main()