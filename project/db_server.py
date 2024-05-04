"""
This script handles login and sign up.
After successful login db server sends client the ip of the game server.
"""
import socket
import traceback
import time
import threading
import pickle

from functions import *
from classes import *

all_to_die = False
PLAYER_ARR: list[Player] = []
LOCK = threading.Lock()
PLAYER_COUNT = 2
GAME = None


def protocol_build_reply(request):
	"""
	Application Business Logic
	function despatcher ! for each code will get to some function that handle specific request
	Handle client request and prepare the reply info
	string:return: reply
	"""

	print("protocol_build_reply not implemnted")
	return b""




def handle_request(request):
	# """
	# Handle client request
	# tuple :return: return message (bytes) to send to client and bool if to close the client socket
	# """
	try:
		request_code = request[:4]
		to_send = protocol_build_reply(request)
		if request_code == b'EXIT':
			return to_send, True
	except Exception as err:
		print(traceback.format_exc())
		to_send =  b'ERRR~008~General error'
	return to_send, False


def handle_client(sock : socket.socket, tid: int , addr):
	"""
	Main client thread loop (in the server),
	:param sock: client socket
	:param tid: thread number
	:param addr: client ip + reply port
	:return: void
	"""
	global all_to_die
	global PLAYER_ARR

	print(f'New Client number {tid} from {addr}')

	# Server hello
	from_player: bytes = recive_by_size(sock)
	hello,money,name = from_player.split(b'~')
	if hello != b"HELLO":
		raise ValueError("Wrong command")
	money = int(money)
	name = name.decode()
	player_index = len(PLAYER_ARR) - 1 # This variable is the index of the player in the PLAYER_ARR array.
	with LOCK:
		PLAYER_ARR.append(Player(addr,len(PLAYER_ARR),money,name))
	send_data(sock,f'HELLO~{PLAYER_COUNT - len(PLAYER_ARR)}'.encode(),tid)

	count = len(PLAYER_ARR)
	while len(PLAYER_ARR) != PLAYER_COUNT:
		if count != len(PLAYER_ARR):
			count = len(PLAYER_ARR)
			send_data(sock,f'HELLO~{PLAYER_COUNT - len(PLAYER_ARR)}'.encode(),tid)

	# Handshake complete 


	if player_index == 0: # Only one thread should create the object and deal the cards.
		GAME = Game(PLAYER_ARR)	
		GAME.deal_cards()
	
	player = PLAYER_ARR[player_index]
	to_send = b'PLYR~' + pickle.dumps(player)
	send_data(sock,to_send,tid)

 
	PLAYER_ARR = []
 
	finish = False
	while not finish:
		if all_to_die:
			print('will close due to main server issue')
			break
		try:
			byte_data = recive_by_size(sock)
			if byte_data == b'':
				print ('Seems client disconnected')
				break
			logtcp('recv', byte_data,tid)

			byte_data = byte_data[9:]   # Remove length field
			to_send , finish = handle_request(byte_data)
			if to_send != '':
				send_data(sock, to_send,tid)
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

	srv_sock.bind(('127.0.0.1', 1235))

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