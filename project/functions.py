"""
This file contains all general function, related to networking
"""

import socket

def logtcp(dir: str,byte_data: bytes,tid = 0 ):
	"""
	log direction, tid and all TCP byte array data
	return: void
	"""
	if dir == 'sent':
		print(bytes(tid) + b' LOG:Sent     >>> ' + byte_data)
	else:
		print(bytes(tid) + b' LOG:Received  <<<    ' + bytes(byte_data))




def send_data(sock: socket.socket,bdata: bytes,tid = 0,):
	"""
	send to client byte array data
	will add 8 bytes message length as first field
	e.g. from 'abcd' will send  b'00000004~abcd'
	return: void
	"""
	bytearray_data = str(len(bdata)).zfill(8).encode() + b'~' + bdata
	sock.send(bytearray_data)
	logtcp('sent',bytearray_data,tid)
	print("")





def recive_by_size(sock: socket.socket) -> bytes:
    
    size = b''
    while not b'~' in size:
        size += sock.recv(4)
    parts = size.split(b'~')
    size = int(parts[0])
    
    msg = parts[1]
    while len(msg) != size:
        
        msg += sock.recv(size)
    logtcp('recv',msg)
    return msg



def sub_tuple(tuple1: tuple[int,int],tuple2:tuple[int,int]) -> tuple[int,...]:
    return tuple([abs(a-b) for a,b in zip(tuple1,tuple2)])