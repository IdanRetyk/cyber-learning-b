import tkinter as tk
from tkinter import ttk
import socket,threading,traceback
import time





def logtcp(dir,tid, byte_data):
	"""
	log direction, tid and all TCP byte array data
	return: void
	"""
	if dir == 'sent':
		print(f'{tid} S LOG:Sent     >>> {byte_data}')
	else:
		print(f'{tid} S LOG:Recieved <<< {byte_data}')




def send_data(sock,tid,bdata):
	"""
	send to client byte array data
	will add 8 bytes message length as first field
	e.g. from 'abcd' will send  b'00000004~abcd'
	return: void
	"""
	bytearray_data = str(len(bdata)).zfill(8).encode() + b'~' + bdata
	sock.send(bytearray_data)
	logtcp('sent',tid, bytearray_data)
	print("")




def check_length(message):
	"""
	check message length
	return: string - error message
	"""
	return b''




def handle_request(data):
    command = data[:5]
    finish = False
    if (command == b'sign_in'):
        to_send = check_sign_in(data[5:])
    elif (command == b'sign_up'):
        to_send = sign_up(data[5:])
    else:
        print("unknown command")
        finish = True
    return to_send,finish





def handle_client(sock, tid , addr):
	"""
	Main client thread loop (in the server),
	:param sock: client socket
	:param tid: thread number
	:param addr: client ip + reply port
	:return: void
	"""
	global all_to_die

	finish = False
	print(f'New Client number {tid} from {addr}')
	while not finish:
		if all_to_die:
			print('will close due to main server issue')
			break
		try:
			byte_data = sock.recv(1000)  # todo improve it to recv by message size
			if byte_data == b'':
				print ('Seems client disconnected')
				break
			logtcp('recv',tid, byte_data)
			err_size = check_length(byte_data)
			if err_size != b'':
				to_send = err_size
			else:
				byte_data = byte_data[9:]   # remove length field
				to_send , finish = handle_request(byte_data)
			if to_send != '':
				send_data(sock, tid , to_send)
			if finish:
				time.sleep(1)
				break
		except socket.error as err:
			print(f'Socket Error exit client loop: err:  {err}')
			break
		except Exception as  err:
			print(f'General Error %s exit client loop: {err}')
			print(traceback.format_exc())
			break

	print(f'Client {tid} Exit')
	sock.close()


def main ():
	global  all_to_die
	"""
	main server loop
	1. accept tcp connection
	2. create thread for each connected new client
	3. wait for all threads
	4. every X clients limit will exit
	"""
	threads = []
	srv_sock = socket.socket()

	srv_sock.bind(('127.0.0.1', 1233))

	srv_sock.listen(20)

	#next line release the port
	srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	i = 1
	while True:
		print('\nMain thread: before accepting ...')
		cli_sock , addr = srv_sock.accept()
		t = threading.Thread(target = handle_client, args=(cli_sock, str(i),addr))
		t.start()
		i+=1
		threads.append(t)
		if i > 100000000:     # for tests change it to 4
			print('\nMain thread: going down for maintenance')
			break

	all_to_die = True
	print('Main thread: waiting to all clints to die')
	for t in threads:
		t.join()
	srv_sock.close()
	print( 'Bye ..')


if __name__ == '__main__':
	main()


