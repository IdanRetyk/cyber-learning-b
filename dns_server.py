import socket

DNS_SERVER_IP = "0.0.0.0"
DNS_SERVER_PORT = 53
DEAFALT_BUFFER_SIZE = 1024
cont = True

def dns_handler(data,addr,sock):
    if b"google" in data :
        #  -----id---------rest of header ---------------------------query block ------response header------------------------------   ip of gvahim
        msg = data[:2] + b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00' + data[12:] + b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x4f\x00\x04\xd4\x8f\x46\x28'
        sock.sendto(msg,addr)
        print(f"sent {msg} to " + str(addr))


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
