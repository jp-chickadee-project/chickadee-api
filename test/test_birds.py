import unittest
import json

from pprint import pprint
from chickadee_tester import ChickadeeTester

class TestBirds(ChickadeeTester):
	def testGetBirds(self):
		response = self.app.get('/api/birds/')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data)
		response = json.loads(response.data)

		self.assertTrue(response[0]['rfid'])
		self.assertTrue(response[0]['bandCombo'])

	def testGetOneBird(self):
		response = self.app.get('/api/birds/011016A269')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data)
		response = json.loads(response.data)
		self.assertEqual(response['rfid'], "011016A269")

		response = self.app.get('/api/birds/nonsense')
		self.assertEqual(response.status_code, 404)
		self.assertTrue(response.data)
		self.assertEqual(response.data.decode(), "404 - Specified rfid does not exist")

	def testBirdOptions(self):
		response = self.app.get('/api/birds/options')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data)

		response = json.loads(response.data)
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

		self.assertEqual(response['species'], ['RBNU', 'BCCH', 'WBNU', None])
		self.assertEqual(response['suspectedSex'], ['female', 'unknown', '', 'male', None])
		self.assertEqual(response['tissueSample'], ['feather', 'none', 'no', None])

if __name__ == "__main__":
	unittest.main()