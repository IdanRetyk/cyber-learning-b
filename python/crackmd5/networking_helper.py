import socket
"""
a module that consists every function that is used for communications
"""

def recv_by_size(sock : socket.socket) -> bytes:
    return sock.recv(1024)
    #TODO actually write this function


def send_data(data: bytes, sock: socket.socket, tid: str):
    bytearray_data = str(len(data)).zfill(8).encode() + b'~' + data
    sock.send(bytearray_data)
    logtcp('sent',tid, bytearray_data)
    print("")

def logtcp(dir ,tid :str, byte_data):
	"""
	log direction, tid and all TCP byte array data
	return: void
	"""
	if dir == 'sent':
		print(f'{tid} S LOG:Sent     >>> {byte_data}')
	else:
		print(f'{tid} S LOG:Recieved <<< {byte_data}')
