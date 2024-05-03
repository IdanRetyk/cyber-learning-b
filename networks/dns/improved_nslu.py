from scapy.layers.inet import UDP,IP,sr1 #type :ignore
from scapy.layers.dns import DNS,DNSQR,DNSRR

import re


def ns_look_up(ip):
    domain = ip


    dns_query = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(qdcount=1, rd=1,qd = 0)/DNSQR(qname=domain)
    response = sr1(dns_query,verbose=0)
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