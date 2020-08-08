import sys
import socket
import threading

def server_loop(lh, lp, rh, rp, rf):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server.bind((lh, lp))

	except AuthenticationException:
		print("[!!] Failed to listen on %s : %d"%(lh, lp))
		print("[!!] Check for other listening sockets or correct permissions.")
		sys.exit(0)

	print("Listening on %s : %d"%(lh, lp))
	server.listen(5)
	while True:
		client_socket, addr = server.accept()
		print("[==>] Received incomming connection from %s : %d"%(addr[0], addr[1]))
		proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, rh, rp, rf))
		proxy_thread.start()

def main():
	if len(sys.argv[1:]) != 5:
		print("Usage: python3 tcp_proxy.py [local host] [local port] [remote host] [remote port] [receive first]")
		print("Example: python3 tcp_proxy.py 127.0.0.1 9000 173.123.5.23 80 True")
		sys.exit(0)
	
	lh = sys.argv[1]
	lp = int(sys.argv[2])
	rh = sys.argv[3]
	rp = int(sys.argv[4])
	rf = sys.argv[5]
	if "True" in rf:
		rf = True
	else:
		rf = False
	
	server_loop(lh, lp, rh, rp, rf)

def proxy_handler(client_socket, rh, rp, rf):
	remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_socket.connect((rh, rp))
	if rf:
		remote_buffer = receive_from(remote_socket)
		hexdump(remote_buffer)
		remote_buffer = response_handler(remote_buffer)
		if len(remote_buffer):
			print("[<==] Sending %d bytes to localhost."%len(remote_buffer))
			client_socket.send(remote_buffer)
	
	while True:
		local_buffer = receive_from(client_socket)
		if len(local_buffer):
			print("[==>] Received %d from localhost."%len(local_buffer))
			hexdump(local_buffer)
			local_buffer = request_handler(local_buffer)
			remote_socket.send(local_buffer)
			print("[==>] send to remote")
		
		remote_buffer = receive_from(remote_socket)
		if len(remote_buffer):
			print("[<==] Receive %d bytes from remote."%len(remote_buffer))
			hexdump(remote_buffer)
			remote_buffer = response_handler(remote_buffer)
			client_socket.send(remote_buffer)
			print("[<==] Send to localhost.")
		
		if not len(remote_buffer) or not len(local_buffer):
			client_socket.close()
			remote_socket.close()
			print("[*] No more data, Closing connection")
			break

def hexdump(src, length=16):
	unicode = ()
	result = []
	digits = 4 if isinstance(src, unicode) else 2
	for i in range(0, len(src), length):
		s = src[i:i+length]
		hexa = b' '.join(["%0*X"%(digits, ord(x)) for x in s])
		text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
		result.append(b"%04X %-8s %s"%(i, length*(digit+1), hexa, text))
		print(b'\n'.join(result)) 

def receive_from(connections):
	buffer = ""
	connections.settimeout(2)
	try:
		while True:
			data = connection.recv(4096)
			if not data:
				break
			
			buffer += data
	
	except:
		pass
	
	return buffer

def request_handler(buffer):
	return buffer

def response_handler(buffer):
	return buffer

main()
