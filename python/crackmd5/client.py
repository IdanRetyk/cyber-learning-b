import socket
import multiprocessing
import os
import subprocess
from subprocess import PIPE
from hashlib import md5

from networking_helper import *

DEBUG = False

if DEBUG:
    CPU_COUNT = 1
    
else:
    CPU_COUNT = multiprocessing.cpu_count()
TARGET: str

class Chunk():
    def __init__(self,range: tuple[int,int],id: int) -> None:
        self.__id = id
        self.__range = range

    
    def get_range(self) -> tuple[int,int]:
        return self.__range
    
    def get_id(self) -> int:
        return self.__id


def communicate_processes(subprocesses: list[subprocess.Popen[bytes]]) -> int | None:
    """Run every process simultaneously using subprocesses.Popen().communicate()

    Args:
        subprocesses (list[subprocess.Popen[bytes]]): list fo processes

    Returns:
        int | None: return answer as int found, else return None.
    """
    answer :int | None = None 
    for sp in subprocesses:
        stdout,_ = sp.communicate()
        # Waiting for process to terminate
        if b"FOUND" in stdout:
            # Found answer
            answer = int(stdout.split(b'~')[1].decode())
            # Kill every other subprocess
            kill_all_processes(subprocesses)
    return answer


def kill_all_processes(ls: list[subprocess.Popen]):
    for sb in ls:
        try:
            sb.kill()
        except:
            pass


def parse_chunks(data :bytes) -> list[Chunk]:
    chunks = data.split(b'!')
    to_return: list[Chunk] = []
    for chunk in chunks:
        if not chunk:
            continue
        start,end,id = [int(f) for f in chunk.split(b'~')[1:]]
        to_return.append(Chunk((start,end),id))
    return to_return


def handshake(sock: socket.socket):
    global TARGET
    send_data(f'HELLO~{CPU_COUNT}'.encode(),sock)
    TARGET = recv_by_size(sock).decode()
    send_data(b'ACK',sock)


def main():
    cli_sock = socket.socket()
    cli_sock.connect(("127.0.0.1",12344))
    
    # Handshake
    handshake(cli_sock)
    
    finish = False
    while not finish:
        
        subprocesses: list[subprocess.Popen[bytes]] = []
        
        data = recv_by_size(cli_sock)
        
        if not data:
            # Server disconnect
            cli_sock.close()
            exit()
        
        # Parse data
        if b"NEW" in data:
            chunks = parse_chunks(data)
        elif b"EXIT" in data:
            kill_all_processes(subprocesses)
            exit()
        else:
            raise Exception("Unknown command")

        # Create subprocess for each chunk
        for chunk in chunks:
            start,end = chunk.get_range()
            sp = subprocess.Popen(["python",f'{os.path.dirname(__file__)}/worker.py',str(start),str(end),TARGET],stdout=PIPE,stderr=PIPE)
            subprocesses.append(sp)
        
        # Run every subprocess simultaneously
        answer = communicate_processes(subprocesses)
        
        if answer:
            to_send = f"FOUND~{answer}".encode()
        else:
            print("#####\nDONE chunk!!!!!!\n######")
            to_send = f"DONE"
            for chunk in chunks:
                to_send += f"~{chunk.get_id()}"
            to_send = to_send.encode()
        send_data(to_send,cli_sock)

if __name__ == "__main__":
    main()