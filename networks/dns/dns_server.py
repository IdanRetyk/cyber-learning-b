import socket
from scapy.layers.dns import DNS, DNSQR, DNSRR  # type: ignore

DNS_SERVER_IP = "0.0.0.0"
DNS_SERVER_PORT = 53
DEFAULT_BUFFER_SIZE = 1024

# DNS records for example
DNS_RECORDS = {
    "google.com.": "142.250.190.78"
}

def build_dns_response(data):
    dns = DNS(data)
    query_name = dns[DNSQR].qname.decode()
    
    response = DNS(id=dns.id,qr=1,opcode=dns.opcode,aa=1,tc=0,d=dns.rd, ra=0,z=0,rcode=0,qdcount=1,ancount=1 if query_name in DNS_RECORDS else 0,nscount=0,arcount=0)
    
    response.qd = dns.qd
    
    if query_name in DNS_RECORDS:
        response.an = DNSRR(rrname=query_name,type='A',rclass='IN',ttl=300,rdlen=4,rdata=DNS_RECORDS[query_name])
    return bytes(response)

def dns_handler(data, addr, sock):
    try:
        response_data = build_dns_response(data)
        sock.sendto(response_data, addr)
        print(f"Sent response to {addr}")
    except Exception as ex:
        print(f"Error handling DNS request: {str(ex)}")

def dns_udp_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print("UDP server successfully started on port", port)
    
    while True:
        try:
            data, addr = server_socket.recvfrom(DEFAULT_BUFFER_SIZE)
            dns_handler(data, addr, server_socket)
            break
        except Exception as ex:
            print(f"Client exception: {str(ex)}")

def main():
    print("Starting UDP server")
    dns_udp_server(DNS_SERVER_IP, DNS_SERVER_PORT)

if __name__ == "__main__":
    main()