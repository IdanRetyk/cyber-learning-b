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


def broadcast(sock : socket.socket,player_arr: list[Player],data: bytes,tid: str):
    for player in player_arr:
        send_data(sock,data,player.get_addr(),tid)


def handle_game(sock : socket.socket, data: bytes,tid: str , addr):
	"""
	Main client thread loop (in the server),
	:param sock: client socket
	:param tid: thread number
	:param addr: client ip + reply port
	:return: void
	"""
 
	# This function will be called after receiving one player.
	# After initializing according to that player, accepting more players until game is full and ready to start
	# At this point the main game loop will start and the game is on.
 
	global all_to_die



	print(f'New Client number {tid} from {addr}')


	code,money,name = data.split(b'~')
	pos = 1
	player_arr: list[Player] = [Player(addr,1,int(money),name.decode())]
	send_data(sock,f'HELLO~{PLAYER_COUNT - len(player_arr)}'.encode(),addr,tid)
 
	# Server waiting for new players. For each player joining broadcast new server hello with current amount of Players.
	from_player,addr = recive_by_size(sock)
	hello,money,name = from_player.split(b'~')
	if hello == b"HELLO" and pos != PLAYER_COUNT: # new player
		pos += 1
		player_arr.append(Player(addr,pos,money,name)) # type:ignore
		to_broadcast = b'HELLO~' + bytes(len(player_arr))
		broadcast(sock,player_arr,to_broadcast,tid)

	# Handshake complete 

	GAME = Game(player_arr)	
	GAME.deal_cards()
	
	player = player_arr[pos - 1]
	to_send = b'PLYR~' + pickle.dumps(player)
	send_data(sock,to_send,tid)


	#TODO implement main game loop
	# finish = False
	# while not finish:
	# 	if all_to_die:
	# 		print('will close due to main server issue')
	# 		break
	# 	try:
	# 		byte_data,a = recive_by_size(sock)
	# 		if byte_data == b'':
	# 			print ('Seems client disconnected')
	# 			break
	# 		logtcp('recv', byte_data,tid)

	# 		byte_data = byte_data[9:]   # Remove length field
	# 		to_send , finish = handle_request(byte_data)
	# 		if to_send != '':
	# 			send_data(sock, to_send,tid)
	# 		if finish:
	# 			time.sleep(1)
	# 			break
	# 	except socket.error as err:
	# 		print(f'Socket Error exit client loop: err:  {err}')
	# 		break
	# 	except Exception as  err:
	# 		print(f'General Error %s exit client loop: {err}')
	# 		print(traceback.format_exc())
	# 		break

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
	srv_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	srv_sock.bind(('127.0.0.1', 1235))

	i = 1
	while True:
		print('\nMain thread: before accepting ...')
		data , addr = srv_sock.recvfrom(1024)
		t = threading.Thread(target = handle_game, args=(srv_sock,data, i,addr))
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