from pymongo import MongoClient
import socketserver
import json

class RequestHandler(socketserver.BaseRequestHandler):
	def sleep_birdfeeder(self, data):
		return
	def restart_birdfeeder(self, data):
		return
	def add_event(self, data):
		self.db.visits.insert_one(data)

		self.db.stations.update_one(
			{"StationID": data["stationID"]},
			{
				"$inc": {"VisitCount": 1},
				"$set": {"Battery": data["battery"]},
				"$set": {"PathTaken": data["path"]}
			}
		)
		self.db.rfids.update_one(
			{"RFID": data["rfid"]},
			{
				"$inc": {"VisitCount": 1}
			}
		)

	cmd_table = {
		'sleep': sleep_birdfeeder,
		'restart' : restart_birdfeeder,
		'event' : add_event,
	}
	mongologin = {
		'host': "euclid.nmu.edu",
		'port': 27017,
		'username': "",
		'password': "",
		'authSource': "chickadees"
	}
	mongo_client = None
	db = None

	def setup(self):
		self.mongo_client = MongoClient(self.mongologin)
		self.db = self.mongo_client.chickadees

	def handle(self):
		self.data = self.request.recv(4096).strip().decode('utf-8')
		print("Recieved request: \"" + self.data + "\" from: "+ str(self.client_address))

		self.data = json.loads(self.data)
		if 'cmd' not in self.data:
			self.request.sendall(b"Invalid request format: missing command")
			return

		cmd = self.data['cmd']

		if cmd in self.cmd_table:
			self.cmd_table[cmd](self, self.data)

	def finish(self):
		self.mongo_client.close()



class ChickadeeServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	_client_whitelist = [
		'127.0.0.1',
		'198.110.204.9' #euclid
	]
	def verify_request(self, request, addr):
		return addr[0] in self._client_whitelist


if __name__ == "__main__":
	server = ChickadeeServer(("localhost", 8127), RequestHandler)
	server.serve_forever()