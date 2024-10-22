import socket
import threading 
import sys
import psutil
import subprocess
from subprocess import PIPE

from networking_helper import *

CPU_COUNT = sys.argv[1] 
TARGET: int
PERCENT: int

class Chunk():
    def __init__(self,range: tuple[int,int],id: int) -> None:
        self.__id = id
        self.__range = range

    
    def get_range(self) -> tuple[int,int]:
        return self.__range
    
    def get_id(self) -> int:
        return self.__id






def parse_chunks(data :bytes) -> list[Chunk]:
    chunks = data.split(b'!')
    to_return: list[Chunk] = []
    for chunk in chunks:
        _,start,end,id = [int(f) for f in chunk.split(b'~')]
        to_return.append(Chunk((start,end),id))
    return to_return


def main():
    cli_sock = socket.socket()
    cli_sock.connect(("127.0.0.1",12344))
    
    # Handshake
    send_data(f'HELLO~{CPU_COUNT}'.encode(),cli_sock)
    
    finish = False
    while not finish:
        data = recv_by_size(cli_sock)
        if b"NEW" in data:
            chunks = parse_chunks(data)
        elif b"EXIT" in data:
            exit()
        else:
            raise Exception("Unknown command")
        subprocesses: list[subprocess.Popen[bytes]] = []
        # Create subprocess for each chunk
        for chunk in chunks:
            start,end = chunk.get_range()
            sp = subprocess.Popen(f"python worker.py {start} {end} {TARGET}",stdout=PIPE,stderr=PIPE)
            subprocesses.append(sp)
        # Run every subprocess simultaneously
        answer :int | None = None 
        for sp in subprocesses:
            stdout,_ = sp.communicate()
            # Waiting for process to terminate
            if "FOUND" in stdout.decode():
                answer = int(stdout.split(b'~')[1].decode())
        if answer:
            to_send = f"FOUND~{answer}".encode()
        else:
            to_send = f"DONE"
            for chunk in chunks:
                to_send += f"~{chunk.get_id()}"
            to_send = to_send.encode()
        send_data(to_send,cli_sock)

if __name__ == "__main__":
    main()