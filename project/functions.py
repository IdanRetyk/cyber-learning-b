"""
This file contains all general function, related to networking
"""

import socket


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


def udp_recv(sock: socket.socket) -> tuple[bytes | None, tuple[str, int] | None]:
    """recvs message.
    If size doesn't match the message, return None

    Returns:
            tuple[bytes | None,tuple[str,int] | None]:message,address if received message, and the size is right. Any other case return NOne,NOne
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

    logtcp("recv",msg)
    return msg, addr


def sub_tuple(tuple1: tuple[int, int], tuple2: tuple[int, int]) -> tuple[int, ...]:
    return tuple([abs(a - b) for a, b in zip(tuple1, tuple2)])
