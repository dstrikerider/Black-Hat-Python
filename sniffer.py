import socket, os
host = "192.168.43.225"
try:
	while True:
		if os.name == "nt":
			socket_protocol = socket.IPPROTO_IP
		else:
			socket_protocol = socket.IPPROTO_ICMP
		
		sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
		sniffer.bind((host, 0))
		sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
		if os.name == "nt":
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVSLL_ON)
		
		print(sniffer.recvfrom(65565))
		print("\n")

except KeyboardInterrupt:
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVSLL_OFF)
