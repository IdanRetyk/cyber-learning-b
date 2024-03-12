# this script find all open ports in range 20-1024 in another computer using syn packeges.

from scapy.all import TCP,IP,sr1,send,sniff
import sys

_IP = sys.argv[1]

open_ports = []

for i in range(20,1024):
    syn_packet = IP(dst=_IP)/TCP(sport = 50,dport=i, seq=123, flags='S')
    syn_ack_packet = sr1(syn_packet,timeout = 1)

    if syn_ack_packet is not None:
        open_ports.append(i)


print (f"{open_ports = }")