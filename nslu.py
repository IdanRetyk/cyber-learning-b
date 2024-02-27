from scapy.layers.inet import IP
from scapy.all import DNS, DNSQR, IP, sr1, UDP


def recv_packet(domain: str):
    dns_packet = IP(dst='8.8.8.8')/UDP(sport=24601,dport=53)/DNS(qd=None,qdcount=1,rd=1,)/DNSQR(qname=domain)
    dns_packet[DNSQR] = DNSQR(qname="www.google.com")
    dns_packet.show()
    response_packet = sr1(dns_packet)
    return response_packet
    

respone = recv_packet("www.google.com")
print(respone)

