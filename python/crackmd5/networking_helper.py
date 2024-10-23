import socket
"""
a module that consists every function that is used for communications
"""

def recv_by_size(sock : socket.socket) -> bytes:
    bdata: bytes = b''
    while b'~' not in bdata:
        bdata += sock.recv(4)
    size,msg = bdata.split(b'~')
    while len(msg) != int(size.decode()):
        msg += sock.recv(512)
    logtcp("recv",msg)
    return msg


def send_data(data: bytes, sock: socket.socket, tid: str = ""):
    
    bytearray_data = str(len(data)).zfill(8).encode() + b'~' + data
    sock.send(bytearray_data)
    logtcp('sent',bytearray_data,tid )
    print("")

def logtcp(dir ,byte_data,tid :str = "" ):
	"""
	log direction, tid and all TCP byte array data
	return: void
	"""
	if dir == 'sent':
		print(f'{tid} S LOG:Sent     >>> {byte_data}')
	else:
		print(f'{tid} S LOG:Recieved <<< {byte_data}')
