from scapy.all import sniff, Raw,send
from scapy.layers.inet import IP, ICMP


SRC_IP = "XXX.XXX.XXX.XXX"
def Check_IP(packet):
    if IP in packet and packet[IP].dst == SRC_IP:
        print(packet.summary())

file_data = sniff(filter='icmp', count=1, prn=Check_IP)[0].getlayer(Raw).load
while True:
    currentPacket = sniff(filter='icmp', count=1, prn=Check_IP, timeout=15)[0].getlayer(Raw).load
    if not currentPacket:
        break
    file_data += currentPacket
    packet = IP(dst=SRC_IP)/ICMP('echo-request')/Raw(load="ACK")
    send(packet)
    

with open("someFile", "wb") as file:
    file.write(file_data)