# this is a dns proxy using the previously written dns server and clinet (nslookup)

from dns_server import dns_udp_server

from scapy.layers.inet import UDP,IP,sr1 #type :ignore
from scapy.layers.dns import DNS,DNSQR,DNSRR

import re,socket

DNS_SERVER_IP = "0.0.0.0"
DNS_SERVER_PORT = 53




def ns_look_up(ip):
    domain = ip
    
    c = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    dns_query = IP(dst=DNS_SERVER_IP) / UDP(dport=53) / DNS(qdcount=1, rd=1,qd = 0)/DNSQR(qname=domain)
    
    c.sendto(dns_query,(DNS_SERVER_IP,DNS_SERVER_PORT))
    
    response = dns_udp_server(DNS_SERVER_IP,DNS_SERVER_PORT)
    handle(response,domain)

        

def is_valid(domain):
    return re.match(r"www.\w+(.\w+)+",domain) is not None



def handle(response_packet,qname):
    number_of_dns_response = response_packet[DNS].ancount
    dnsrr_list = response_packet.an
    
    # Check if the response contain Canonical name
    if dnsrr_list[0].type == 5:
        print("Name:   ", dnsrr_list[0].rdata.decode())
        print("Address:  ", end="")
        # Print all dnsrrs
        for dnsrr in dnsrr_list[1:]:
            print(dnsrr.rdata)
        print("Aliases: ", qname)
    else:  # if does not contain Canonical name
        print("Name:   ", qname)
        print("Address:  ", end="")
        # Print all dnsrrs
        for dnsrr in dnsrr_list:
            if (dnsrr != None):
                print(dnsrr.rdata)  



def main():
    
    while True:
        quit = False
        data = input("> ")
        
        if (data.lower() in ("quit()", "exit()")):
            print()
            break
        
        while not is_valid(data):
            print("Please enter a valid domain")
            data = input("> ")
            if (data.lower() in ("quit()", "exit()")):
                quit = True
        if (not quit):
            ns_look_up(data)
        

if __name__ == "__main__":
    main()