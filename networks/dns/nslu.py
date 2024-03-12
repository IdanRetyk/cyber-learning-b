from scapy.all import UDP,DNS,DNSQR,IP,sr1,DNSRR
domain = input("Enter addr \n")


dns_query = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))
response = sr1(dns_query)
if response[DNSRR].type == 1: 
    print(response[DNSRR].rdata)
elif response[DNSRR].type == 5:
    print(response[DNSRR][1].rdata)