import socket

target_host = '127.0.0.1'
target_port = 80
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'ABBCCCDDDD', (target_host, target_port))
addr, data = client.recvfrom(4096)
print(data)

