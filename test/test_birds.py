import unittest
import json

from pprint import pprint
from chickadee_tester import ChickadeeTester

class TestBirds(ChickadeeTester):
	def setUp(self):
		super(TestBirds, self).setUp()

		self.testbird = {
			"rfid": "TESTBIRD",
			"bandCombo": "#v/v0",
			"species": "RBNU", 
			"suspectedSex": "female", 
			"tailLength": 37
		}
		
	def tearDown(self):
		self.app.delete('/api/birds/TESTBIRD')

	def testGetAll(self):
		response = self.app.get('/api/birds/')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data)
		response = json.loads(response.data.decode())

		self.assertTrue(response[0]['rfid'])
		self.assertTrue(response[0]['bandCombo'])

	def testGetOne(self):
		response = self.app.get('/api/birds/011016A269')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode().decode())
		self.assertEqual(response['rfid'], "011016A269")

		response = self.app.get('/api/birds/nonsense')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data.decode(), "404 - Specified rfid does not exist")

	def testGetOptions(self):
		response = self.app.get('/api/birds/options')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data)

		response = json.loads(response.data.decode())
		self.assertTrue('James' in response['banders'])
		self.assertTrue('Dershem' in response['banders'])
		self.assertTrue('Bertucci' in response['banders'])
		self.assertTrue('SJS' in response['banders'])
		self.assertTrue('Lindsay' in response['banders'])

		self.assertEqual(response['bands']['A'], 'AZURE darvic')
		self.assertEqual(response['bands']['av'], 'azure violet stripe RFID')
		self.assertEqual(response['bands']['yb'], 'yellow black stripe RFID')

		self.assertTrue('Carpenter Net' in response['captureSite'])
		self.assertTrue('Cliffside Net' in response['captureSite'])
		self.assertTrue('Riley Net' in response['captureSite'])
		self.assertTrue('Sproull Net' in response['captureSite'])

		self.assertTrue('RBNU' in response['species'])
		self.assertTrue('BCCH' in response['species'])
		self.assertTrue('WBNU' in response['species'])

		self.assertTrue('female' in response['species'])
		self.assertTrue('male' in response['species'])
		self.assertTrue('unknown' in response['species'])

		self.assertTrue('feather' in response['tissueSample'])

	def testPost(self):
		response = self.app.post('/api/birds/', data=self.testbird)

		self.assertEqual(response.status_code, 201)
		self.assertTrue(response.data)
		response = json.loads(response.data.decode())

		for key in self.testbird:
			self.assertEqual(self.testbird[key], response[key])

		#Test with missing rfid
		invalidbird = self.testbird.copy()
		invalidbird["rfid"] = ""
		response = self.app.post('/api/birds/', data=invalidbird)

		self.assertEqual(response.status_code, 400)
		self.assertTrue(response.data)
		self.assertEqual(response.data.decode(), 'rfid not supplied')

	def testPut(self):
		self.app.post('/api/birds/', data=self.testbird)

		temp = self.testbird.copy()
		temp["billDepth"] = 3.5
		temp["billLength"] = 10.3
		temp["billWidth"] = 3.4
		temp["birdWeight"] = 1
		response = self.app.put('/api/birds/TESTBIRD', data=temp)

		self.assertEqual(response.status_code, 201)
		self.assertTrue(response.data)
		response = json.loads(response.data.decode())

		for key in temp:
			self.assertEqual(temp[key], response[key])

		temp["rfid"] = ""
		response = self.app.post('/api/birds/', data=temp)

		self.assertEqual(response.status_code, 400)
		self.assertTrue(response.data)
		self.assertEqual(response.data.decode(), 'rfid not supplied')

	def testDelete(self):
		self.app.post('/api/birds/', data=self.testbird)

		response = self.app.delete('/api/birds/TESTBIRD')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.data.decode(), '')

		response = self.app.get('/api/birds/TESTBIRD')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data.decode(), "404 - Specified rfid does not exist")

if __name__ == "__main__":
	unittest.main()