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


def udp_recv(sock: socket.socket,expected_code: str = "") -> tuple[bytes | None, tuple[str, int] | None]:
    """recvs message.
    If size doesn't match the message, return None
    If got the wrong message type return none.
    
    Returns:
            tuple[bytes | None,tuple[str,int] | None]:message,address if received message, code is correct, and the size is right. Any other case return NOne,NOne
    """
    sock.settimeout(2)
    try:
        msg, addr = sock.recvfrom(1024)
    except TimeoutError:
        logtcp("recv", b"None")
        return None, None
    fields = msg.split(b"~")
    size = int(fields[0])
    msg = b"~".join(fields[1:])
    if size != len(msg):
        logtcp("recv", msg + b" Wrong Size")
        return None, None
    if msg.split(b'~')[1] != expected_code.encode():
        logtcp("recv",msg + b'~expected' + expected_code.encode())
        return None,None
    logtcp("recv",msg)
    return msg, addr


def sub_tuple(tuple1: tuple[int, int], tuple2: tuple[int, int]) -> tuple[int, ...]:
    return tuple([abs(a - b) for a, b in zip(tuple1, tuple2)])


def broadcast(sock: socket.socket, player_arr: list[Player], data: bytes, tid: str,support_ack:bool = False):
    """send all players in player_arr, a message. 
        if support_ack:
            will only finish function when every single player send an ack back.

    Args:
        sock (socket.socket): socket
        player_arr (list[Player]): list of players
        data (bytes): data to broadcast
        tid (str): thread id
        support_ack (bool, optional): weather of not check for ack from players. Defaults to False.
    """
    if support_ack:
        """
        This will send all players a message. Keep track evry player who send ack. 
        Continue to send the message to every player who didn't sent ack yet.
        After receiving ack from a player, send them ack back according to the ack-ack architecture.
        """
        recv_arr: list[bool] = [False] * PLAYER_COUNT
        while False in recv_arr: # Until every client sent ack
            for i in range(PLAYER_COUNT):
                if not recv_arr[i]:
                    p = player_arr[i]
                    send_data(sock,data,p.get_addr(),tid)
                    from_client,addr = udp_recv(sock,"ACK")
                    if from_client is not None:
                        recv_arr[index_address(player_arr,addr)] = True
                        send_data(sock,b'ACK',addr,tid)
    
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
    raise ValueError("Value not found")
