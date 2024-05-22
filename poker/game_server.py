"""
This server handles the actual poker.
"""

import socket
import traceback
import time
import threading
import pickle
from base64 import b64encode,b64decode

from functions import *
from classes import *




all_to_die = False

LOCK = threading.Lock()
PLAYER_COUNT = 4
OPEN_NEW_GAME: bool = True # When this var is true, any new client that connects will start a new game
                            #if its false, new client will be send to an already existing waiting room


def protocol_build_reply(request):
    """
    Application Business Logic
    function despatcher ! for each code will get to some function that handle specific request
    Handle client request and prepare the reply info
    string:return: reply
    """

    print("protocol_build_reply not implemnted")
    return b""


def handle_move(from_player: bytes,player_position: int,game : Game) -> tuple[bytes,str]:
    # """
    # Handle client request
    # tuple :return: return message (bytes) to send to client, and str representing move type (bet,check,fold)
    # """
    fields = from_player.split(b'~')
    if fields[0] != b'MOVE':
        raise ValueError()
    if fields[1] == b'-1': # Fold
        game.get_players()[player_position].fold()
        return f"MOVE~-1~{player_position}".encode(),"fold"
    if fields[1] == b'0' :# Check
        return f"MOVE~0~{player_position}".encode(),"check"
    else: 
        if int(fields[1]) <= game.get_bet_size(): # Call/All in
            game.change_pot(int(fields[1]))
            game.get_players()[player_position].change_money(-int(fields[1]))
            game.get_players()[player_position].set_curr_bet(int(fields[1]))
            return f"MOVE~{int(fields[1])}~{player_position}".encode(),"call"
        else: # Bet size
            game.change_pot(int(fields[1]))
            game.get_players()[player_position].change_money(-int(fields[1]))
            game.get_players()[player_position].set_curr_bet(int(fields[1]))
            game.set_bet_size(int(fields[1]))
            return f"MOVE~{int(fields[1])}~{player_position}".encode(),"bet"


def waiting_room(sock: socket.socket, data: bytes,addr,tid: str) -> Game:
    """This function accept new players into an existing game. 
    The function will end only when a game is full.

    Args:
        sock (socket.socket): socket
        data (bytes): first player client hello
        addr (_type_): first client address
        tid (str): thread id

    Returns:
        Game: game object with all the players in it.
    """
    code, money, name = data.split(b"~")
    pos = 1
    player_arr: list[Player] = [Player(addr, 1, int(money), name.decode())]
    send_data(sock,b"HELLO~" + str(PLAYER_COUNT - 1).encode(),addr,tid)
    
    # Server waiting for new players. For each player joining broadcast new server hello with current amount of Players.
    while len(player_arr) != PLAYER_COUNT:
        from_player, addr = udp_recv(sock)
        if from_player is not None:
            code, money, name = from_player.split(b"~")  # type:ignore
        if code == b"HELLO" and pos != PLAYER_COUNT and from_player is not None and index_address(player_arr,addr) == -1: # Add player to the game
            pos += 1
            player_arr.append(Player(addr, pos, int(money), name))  # type:ignore
            to_broadcast = b"HELLO~" + str(PLAYER_COUNT - len(player_arr)).encode()
            broadcast(sock, player_arr, to_broadcast, tid)
    
    print("Waiting room full")# Waiting room full
    return Game(player_arr)



def do_betting_round(sock: socket.socket,game: Game,turn: int,tid: str) -> int:
    """
    Do betting round. Send to current player TURN msg, recieve MOVE msg and handle it, broadcast MOVE msg.
    Will exit function when round bet is over (its the turn of the last player who bet).

    Return _int_ : -1 if on player is left alone, -2 if one player exited (in that case end game).
    oterwise return the index of the winning player.
    """
    count = 0
    addr_list = game.get_addresses_list()
    while count < len(game.get_players()): 
        if game.players_in_game() == 1:
            return game.get_winner()
        if game.get_players()[turn].is_playing():
            send_data_ack(sock,f"TURN~{game.get_bet_size()}".encode(),addr_list[turn],"MOVE")
            from_player,a = recv_ack(sock,"MOVE",[addr_list[turn]])
            if from_player == b'EXIT':
                return -2
            to_broadcast,move_type = handle_move(from_player,turn,game)
            broadcast(sock,game.get_players(),to_broadcast,tid,addr_list)
            if move_type == 'bet':
                count = 1
            else:
                count += 1
        else:
            count += 1
        turn += 1
        turn %= PLAYER_COUNT
    
    game.set_bet_size(0)
    return game.get_winner()



def handle_win(game: Game,winner_list : list[int],show_cards: bool = False):
    """Give winners the pot.

    Args:
        game (Game): _description_
        winner_list (list[int]): _description_
        show_cards (bool, optional): _description_. Defaults to False.
    """
    pot = game.empty_pot()
    for player in game.get_players():
        pot += player.get_curr_bet()
        player.set_curr_bet(0)

    for winner_index in winner_list:
        game.get_players()[winner_index].change_money(pot // len(winner_list)) # Transfer money in the pot into winner's money


def restart(sock: socket.socket,game: Game):
    game.restart(PLAYER_COUNT)
    pickled_game =  b64encode(pickle.dumps(game))
    print(pickle.loads(b64decode(pickled_game)))
    for i in range(len(game.get_players())):
        send_data_ack(sock,f'GAME~{pickled_game.decode()}~{i}'.encode(),game.get_addresses_list()[i],"MOVE")
    blinds(game)



def handle_game(sock: socket.socket, data: bytes, tid: str, addr):
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
    global OPEN_NEW_GAME

    print(f"New Client number {tid} from {addr}")

    game = waiting_room(sock,data,addr,tid)

    
    bytes_game: bytes = b64encode(pickle.dumps(game))
    p_arr = game.get_players()
    
    # Send each player the game object, with their index in the player array
    recv_arr: list[bool] = [False] * PLAYER_COUNT
    while False in recv_arr: # Until every client sent ack
        for i in range(PLAYER_COUNT):
            if not recv_arr[i]:
                p = p_arr[i]
                to_send = b'GAME~' + bytes_game +b'~'+ str(p_arr.index(p)).encode()
                send_data(sock,to_send,p.get_addr(),tid)
                from_client,addr = udp_recv(sock,"ACK",game.get_addresses_list())
                if from_client is not None:
                    recv_arr[index_address(p_arr,addr)] = True
                    send_data(sock,b'ACK',addr,tid)

    print("HANDSHAKE complete")
    # OPEN_NEW_GAME = True
    
    #Recive blinds
    blinds(game)
    
    
    finish = False
    while not finish:
        
        if all_to_die:
            print('will close due to main server issue')
            break
        try:
            
            # Preflop betting
            turn = 2 % PLAYER_COUNT
            possible_winner = do_betting_round(sock,game,turn,tid)
            if possible_winner == -2: # Exit
                broadcast(sock,game.get_players(),b'EXIT',tid)
                finish = True
                continue
            if possible_winner != -1: # There is a winner
                broadcast(sock,game.get_players(),b'WINNER~' + str(possible_winner).encode(),tid)
                handle_win(game,[possible_winner],show_cards=True)
                restart(sock,game)
                continue
            
            game.show_flop()
            broadcast(sock,game.get_players(),b'CARDS~' + b64encode(pickle.dumps(game.get_community_cards())),tid)
            
            
            # Flop betting
            turn = 0
            possible_winner = do_betting_round(sock,game,turn,tid)
            if possible_winner == -2: # Exit
                broadcast(sock,game.get_players(),b'EXIT',tid)
                finish = True
                continue
            if possible_winner != -1: # There is a winner
                broadcast(sock,game.get_players(),b'WINNER~' + str(possible_winner).encode(),tid)
                handle_win(game,[possible_winner],show_cards=True)
                restart(sock,game)
                continue
            game.show_turn()
            broadcast(sock,game.get_players(),b'CARDS~' + b64encode(pickle.dumps(game.get_community_cards())),tid)
            
            
            # Turn betting
            turn = 0
            possible_winner = do_betting_round(sock,game,turn,tid)
            if possible_winner == -2: # Exit
                broadcast(sock,game.get_players(),b'EXIT',tid)
                finish = True
                continue
            if possible_winner != -1: # There is a winner
                broadcast(sock,game.get_players(),b'WINNER~' + str(possible_winner).encode(),tid)
                handle_win(game,[possible_winner],show_cards=True)
                restart(sock,game)
                continue
            game.show_river()
            broadcast(sock,game.get_players(),b'CARDS~' + b64encode(pickle.dumps(game.get_community_cards())),tid)
            
            
            # River betting
            turn = 0
            possible_winner = do_betting_round(sock,game,turn,tid)
            if possible_winner == -2: # Exit
                broadcast(sock,game.get_players(),b'EXIT',tid)
                finish = True
                continue
            if possible_winner != -1: # There is a winner
                broadcast(sock,game.get_players(),b'WINNER~' + str(possible_winner).encode(),tid)
                restart(sock,game)
                continue

            winner_list = game.calculate_winners()
            to_send = b'WINNER~END'
            for winner in winner_list:
                to_send += b'~' + str(winner).encode()
            broadcast(sock,game.get_players(),to_send,tid)
            handle_win(game,winner_list,show_cards=True)
            
            restart(sock,game)

        except KeyboardInterrupt:
            broadcast(sock,game.get_players(),b'EXIT',tid)
            finish = True
            sock.close()
            raise KeyboardInterrupt()
        except socket.error as err:
            print(f'Socket Error exit client loop: err:  {err}')
            break
        except Exception as  err:
            print(f'General Error %s exit client loop: {err}')
            print(traceback.format_exc())
        

    print(f"Client {tid} Exit")
    sock.close()


def main():
    global all_to_die,OPEN_NEW_GAME
    """
    main server loop
    1. accept tcp connection
    2. create thread for each connected new client
    3. wait for all threads
    4. every X clients limit will exit
    """
    threads = []
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    srv_sock.bind(("127.0.0.1", 1235))

    i = 1
    while True:
        data = None
        if OPEN_NEW_GAME:
            print("\nMain thread: before accepting ...")
            while data is None:
                data, addr = udp_recv(srv_sock,"HELLO")
            OPEN_NEW_GAME = False
            t = threading.Thread(target=handle_game, args=(srv_sock, data, str(i), addr))  # type: ignore
            t.start()
            i += 1
            threads.append(t)
            if i > 100000000:  # for tests change it to 4
                print("\nMain thread: going down for maintenance")
                break

    all_to_die = True
    print("Main thread: waiting to all clints to die")
    for t in threads:
        t.join()
    srv_sock.close()
    print("Bye ..")


if __name__ == "__main__":
    main()