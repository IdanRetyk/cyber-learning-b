"""
This file contains all general function, related to networking
"""

import socket
from classes import *
from game_server import PLAYER_COUNT


def logtcp(dir: str, byte_data: bytes, tid: str = ""):
    """
    log direction, tid and all TCP byte array data
    return: void
    """
    if dir == "sent":
        print(tid.encode() + b" LOG:Sent     >>> " + byte_data)
    else:
        print(tid.encode() + b" LOG:Received  <<<    " + bytes(byte_data))


def send_data(sock: socket.socket, bdata: bytes, addr, tid: str = "0"):
    """
    send to client byte array data
    will add 8 bytes message length as first field
    e.g. from 'abcd' will send  b'00000004~abcd'
    return: void
    """
    bytearray_data = str(len(bdata)).zfill(8).encode() + b"~" + bdata
    sock.sendto(bytearray_data, addr)
    logtcp("sent", bytearray_data, tid)
    print("")


def send_data_ack(sock: socket.socket,bdata: bytes,addr,exit_code: str | None = "ack",tid: str = "0",addr_list = []):
    # Exit code - the expected code, after the ack
    
    response: bytes | None = None
    while response != b'ACK':
        send_data(sock,bdata,addr,tid)
        if exit_code is None:
            response,a = udp_recv(sock,expected_addrs=addr_list)
        else:
            response,a = udp_recv(sock,["ACK",exit_code],addr_list)



def recv_ack(sock: socket.socket,expected_codes : list[str] | str = "ACK",expected_addrs: list[tuple[str,int]] = []) -> tuple[bytes, tuple[str, int]]:
    if isinstance(expected_codes,str):
        expected_codes = [expected_codes]
    data,a = udp_recv(sock,expected_codes,expected_addrs)
    msg = data
    if data != None:
        send_data(sock,b'ACK',a)
    while data == None:
        data,a = udp_recv(sock,expected_codes,expected_addrs)
        if data is not None:
            msg = data
            send_data(sock,b'ACK',a)
    
    return msg,a #type:ignore


def udp_recv(sock: socket.socket,expected_codes: list[str] | str = [],expected_addrs: list[tuple[str,int]] = []) -> tuple[bytes | None, tuple[str, int] | None]:
    """recvs message.
    If size doesn't match the message, return None
    If got the wrong message type return none.
    If the message is from a wrong address, return None.
    Returns:
            tuple[bytes | None,tuple[str,int] | None]:message,address if received message, code is correct, from the right address, and the size is right.
            Any other case return NOne,NOne
    """
    
    if isinstance(expected_codes,str):
        expected_codes = [expected_codes]
    
    
    sock.settimeout(0.5)
    try:
        msg, addr = sock.recvfrom(1024)
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except TimeoutError:
        logtcp("recv", b"None")
        return None, None
    fields = msg.split(b"~")
    size = int(fields[0])
    msg = b"~".join(fields[1:])
    
    if size != len(msg): # Check size field.
        logtcp("recv", msg + b" Wrong Size")
        return None, None
    
    if msg.split(b'~')[0].decode() not in expected_codes and len(expected_codes) > 0: # Check if the message has the correct code
        logtcp("recv",msg + b'~expected ' + str(expected_codes).encode())
        return None,None
    
    if addr not in expected_addrs and len(expected_addrs) > 0: # Check if the message was recieved from a user.
        logtcp("recv",b'msg was sent from wrong user')
        return None,None
    logtcp("recv",msg)
    return msg, addr


def sub_tuple(tuple1: tuple[int, int], tuple2: tuple[int, int]) -> tuple[int, ...]:
    return tuple([abs(a - b) for a, b in zip(tuple1, tuple2)])


def broadcast(sock: socket.socket, player_arr: list[Player], data: bytes, tid: str,addrs_list: list[tuple[str,int]] = [],support_ack:bool = False):
    """send all players in player_arr, a message. 
        if support_ack:
            will only finish function when every single player send an ack back.

    Args:
        sock (socket.socket): socket
        player_arr (list[Player]): list of players
        data (bytes): data to broadcast
        tid (str): thread id
        addrs_list (list[tuple[str,int]]): list of the address from which we expect to recive messages.
        support_ack (bool, optional): weather of not check for ack from players. Defaults to False.
    """
    if support_ack:
        """
        This will send all players a message. Keep track evry player who send ack. 
        Continue to send the message to every player who didn't sent ack yet.
        """
        for player in player_arr:
            send_data_ack(sock,data,player.get_addr())

    else:
        for player in player_arr:
            send_data(sock, data, player.get_addr(), tid)


def index_address(player_arr: list[Player],addr) -> int:
    """recv player_arr and return the index at which the player has the given address

    Args:
        player_arr (_type_): _description_
    """
    
    for i in range(len(player_arr)):
        if player_arr[i].get_addr() == addr:
            return i
    return -1


def blinds(game: Game):
    """Takes care of the blinds

    Args:
        game (Game): _description_
    """
    s,b = game.get_blind(False),game.get_blind(True)
    game.get_players()[0].change_money(-s)
    game.get_players()[1].change_money(-b)
    game.set_bet_size(b)
    game.get_players()[0].set_curr_bet(s)
    game.get_players()[1].set_curr_bet(b)