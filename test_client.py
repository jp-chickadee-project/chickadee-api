import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8127))

data = {
	'cd': 'sleep',
	'id': 'CRC'
}

sock.sendall(bytes(json.dumps(data), 'utf-8'))
print(sock.recv(4096).decode('utf-8'))