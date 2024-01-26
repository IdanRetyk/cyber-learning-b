import socket

DNS_SERVER_IP = "0.0.0.0"
DNS_SERVER_PORT = 53
DEAFALT_BUFFER_SIZE = 1024


def dns_handler(data,addr,sock):
    msg = data + b'212.123.70.40'
    sock.sendto(msg,addr)
    print("sent response to " + str(addr))


def dns_udp_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip,port))
    print("UDP server succefully started")
    while True:
        try:
            data,addr = server_socket.recvfrom(DEAFALT_BUFFER_SIZE)
            dns_handler(data,addr,server_socket)
        except Exception as ex:
            print("clinet execption! %s" % (str(ex)))
    
    
def main():
    print("staring udp server")
    dns_udp_server(DNS_SERVER_IP,DNS_SERVER_PORT)
    
if __name__ == "__main__":
    main()
