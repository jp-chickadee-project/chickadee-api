from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import mysql.connector as sql
import json

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_PUT(self):
		self.send_response(200)

	def do_POST(self):
		self.send_response(200)

	def do_DELETE(self):
		self.send_response(200)


class ChickadeeServer(ThreadingMixIn, HTTPServer):
	_client_whitelist = [
		'127.0.0.1',
		'198.110.204.9' #euclid
	]
	def verify_request(self, request, addr):
		return addr[0] in self._client_whitelist

if __name__ == "__main__":
	server = ChickadeeServer(("localhost", 8127), RequestHandler)
	server.serve_forever()