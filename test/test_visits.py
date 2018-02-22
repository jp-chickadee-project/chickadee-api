import unittest
import json

from chickadee_tester import ChickadeeTester

class TestVisits(ChickadeeTester):
	def testGetRange(self):
		#test good range
		response = self.app.get('/api/visits/?start=1487635200&end=1487689900')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 136)

		#test invalid ranges:

		#end less than start
		response = self.app.get('/api/visits/?start=1487689900&end=1487635200')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.decode(), "Bad time-range specification")

		#no start
		response = self.app.get('/api/visits/?end=1487635200')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.decode(), "Bad time-range specification")

		#no end
		response = self.app.get('/api/visits/?start=1487689900')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.decode(), "Bad time-range specification")

		#neither
		response = self.app.get('/api/visits/')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.decode(), "Bad time-range specification")

		#test combinations of rfid and feederID
		response = self.app.get('/api/visits/?start=1487635200&end=1487689900&rfid=0700EE1396&feederID=RILE')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 13)

		response = self.app.get('/api/visits/?start=1487635200&end=1487689900&rfid=0700EE1396')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 13)

		response = self.app.get('/api/visits/?start=1487635200&end=1487689900&feederID=RILE')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 47)

		response = self.app.get('/api/visits/?start=1487635200&end=1487689900&rfid=0700EE1396&feederID=nonsense')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 0)

		response = self.app.get('/api/visits/?start=1487635200&end=1487689900&rfid=nonsense')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 0)


	def testGetLatest(self):
		#test default
		response = self.app.get('/api/visits/latest')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 10)
		self.assertTrue(response[0]["rfid"])
		self.assertTrue(response[0]["feederID"])

		#test limit
		response = self.app.get('/api/visits/latest?limit=100')
		self.assertEqual(response.status_code, 200)
		response = json.loads(response.data.decode())
		self.assertEqual(len(response), 100)

if __name__ == "__main__":
	unittest.main()