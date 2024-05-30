import struct
import socket
import netifaces as nfp

def get_broadcast_address(interface="en1"):
    ifaddresses = nfp.ifaddresses(interface)
    
    ip_info = ifaddresses[nfp.AF_INET][0]
    ip_address = ip_info['addr']
    netmask = ip_info['netmask']
    
    # Convert IP address and netmask to binary format
    ip_binary = struct.unpack('>I', socket.inet_aton(ip_address))[0]
    netmask_binary = struct.unpack('>I', socket.inet_aton(netmask))[0]
    
    # Calculate the broadcast address
    broadcast_binary = ip_binary | ~netmask_binary
    broadcast_address = socket.inet_ntoa(struct.pack('>I', broadcast_binary & 0xFFFFFFFF))
    
    return broadcast_address

c = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

c.sendto(b'hello',(get_broadcast_address(),1234))