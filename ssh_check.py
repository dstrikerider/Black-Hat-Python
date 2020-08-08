import threading
import paramiko
import subprocess
import sys

def ssh_command(ip, user, passwd, command):
	try:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
		client.connect(ip, username=user, password=passwd)
		ssh_session = client.get_transport().open_session()
	
	except paramiko.ssh_exception.AuthenticationException:
		print('\n\n##### Invalid Credentials - Access Denied #####')
		sys.exit(0)
	
	except paramiko.ssh_exception.NoValidConnectionsError:
		print('\n\n##### Unable to Connect with the Host IP #####')
		sys.exit(0)
	
	if ssh_session.active:
		ssh_session.exec_command(command)
		print('\n\n##### Access Granted #####\n\n')	
		print(ssh_session.recv(1024).decode())
		return

def main():
	uname = input('SSH User-Name: ')
	pname = input('SSH Pass Word: ')
	ip = input('SSH Host IP: ') 
	print('\n\n##### Checking Responses #####')
	ssh_command(ip, uname, pname, 'id')

main()
