import socket
import threading
import traceback
import time
import sys
from networking_helper import *


if len(sys.argv) != 2:
    print("Wrong Usage.")
    exit()

TARGET: str = sys.argv[1]
all_to_die: bool = False
CHUNK_SIZE = 10_000_000

class Chunk():
    count: int = 0
    def __init__(self,range: tuple[int,int]) -> None:
        self.__id = Chunk.count
        self.__range = range
        self.__sent: bool = False
        self.__done: bool = False
        Chunk.count += 1
    
    def get_range(self) -> tuple[int,int]:
        return self.__range
    
    def get_id(self) -> int:
        return self.__id
    
    def if_done(self) -> bool:
        return self.__done
    
    def if_sent(self) -> bool:
        return self.__sent
    
    def mark_sent(self):
        self.__sent = True
    
    def mark_unsent(self):
        self.__sent = False
    
    def make_done(self):
        self.__sent = True
        self.__done = True


class Client_info():
    #Struct
    def __init__(self,sock: socket.socket,cpu_count: int) -> None:
        self.__sock = sock
        self.__cpu_count = cpu_count
        self.__jobs: list[int] = [] # Every chunk_id that this client is assigned.
    
    def get_sock(self) -> socket.socket:
        return self.__sock

    def set_sock(self, sock: socket.socket):
        self.__sock = sock

    def get_cpu_count(self) -> int:
        return self.__cpu_count

    def set_cpu_count(self, cpu_count: int):
        self.__cpu_count = cpu_count
    
    def add_job(self,job: int):
        self.__jobs.append(job)
    
    def remove_job(self,job: int):
        self.__jobs.remove(job)

    def get_jobs(self) -> list[int]:
        return self.__jobs



class Server():
    
    def __init__(self) -> None:
        self.chunks = self.get_chunks()
        self.clients: list[Client_info] = [] 
        self.tstart: float = time.time()
    
    def get_chunks(self) -> list[Chunk]:
        chunks: list[Chunk] = []
        for i in range(10_000_000_000//CHUNK_SIZE):
            chunks.append(Chunk((10_000_000 * i,10_000_000 * (i + 1))))
            
        return chunks

    def get_next_chunk(self) -> Chunk | None: 
        global all_to_die
        for chunk in self.chunks:
            if not chunk.if_sent():
                return chunk
        return None
    
    def get_client_via_sock(self, sock: socket.socket) -> Client_info:
        for cli in self.clients:
            if cli.get_sock() == sock:
                return cli
        raise ValueError()


    def handshake(self,sock: socket.socket,tid: int) -> bool:
        data = recv_by_size(sock,str(tid)).split(b'~')
        if not data:
            return True
        _,cpu_count = data
        cpu_count = int(cpu_count)
        self.clients.append(Client_info(sock,cpu_count))
        send_data(TARGET.encode(),sock,str(tid))
        recv_by_size(sock,str(tid))
        
        
        # Send first chunks
        to_send: bytes = b''
        for _ in range(cpu_count):
            chunk = self.get_next_chunk()
            if not chunk:
                # Finished
                return True
            self.get_client_via_sock(sock).add_job(chunk.get_id())
            start,end = chunk.get_range()
            to_send += f'NEW~{start}~{end}~{chunk.get_id()}!'.encode()
            chunk.mark_sent()
        send_data(to_send,sock,str(tid))
        return False
    
    
    def handle_request(self,data :bytes,tid: int) -> tuple[bytes,bool]:
        """_summary_

        Args:
            data (bytes): _description_

        Returns:
            tuple[bytes,bool]: data to send user, finish
        """
        to_send: bytes = b''
        finish = False
        fields = data.split(b'~')
        command = fields[0]
        curr_cli: Client_info = self.clients[tid - 1]
        match command:
            case b"DONE":
                # message consists of every chunk that client has finished.
                #DONE~<chunk_id_1>~<chunk_id_2>~.....
                
                # Mark jobs as done.
                for chunk_id in fields[1:]:
                    self.chunks[int(chunk_id)].make_done()
                    curr_cli.remove_job(int(chunk_id))
                
                # Send new jobs.
                # NEW~<start_range>~<end_range>~<chunk_id>!
                for _ in range(curr_cli.get_cpu_count()):
                    chunk = self.get_next_chunk()
                    if chunk:
                        curr_cli.add_job(chunk.get_id())
                        start,end = chunk.get_range()
                        to_send += f'NEW~{start}~{end}~{chunk.get_id()}!'.encode()
                        chunk.mark_sent()
                        
                    else:
                        finish = True
                if finish:
                    self._exit()
            case b"FOUND":
                self.tend: float = time.time()
                answer = int(fields[1])
                self.found_answer(answer)
                self._exit()
                finish = True
            case _:
                to_send = b'Unknown command'
        
        return to_send,finish


    def handle_client(self,sock: socket.socket,addr: tuple[str,int], tid: str):
        global all_to_die
        
        finish = False
        print(f"New client number {tid} from {addr}")
        finish = self.handshake(sock,int(tid))
        while not finish:
            if all_to_die:
                break
            try:
                bdata: bytes = recv_by_size(sock,str(tid))
                if not bdata:
                    print(f"Client {tid} disconnected")
                    client: Client_info = self.get_client_via_sock(sock)
                    # If client disconnect, mark all its jobs as unsent. After this, they will be reassigned.
                    for i in client.get_jobs():
                        self.chunks[i].mark_unsent()
                    finish = True
                    break
                to_send,finish = self.handle_request(bdata,int(tid))
                if finish:
                    break
                if to_send:
                    send_data(to_send,sock,tid)
                
                if self.chunks[-1].if_done():
                    # Searched all the chunks
                    finish = True
                    print("-1")
                
            except socket.error as err:
                print(f'Socket Error exit client loop: err:  {err}')
                break
            except Exception as  err:
                print(f'General Error %s exit client loop: {err}')
                print(traceback.format_exc())
                break



    def main(self):
        global all_to_die
        
        threads: list[threading.Thread] = []
        srv_sock :socket.socket = socket.socket()
        
        srv_sock.bind(("127.0.0.1",12344))
        srv_sock.listen(20)

        srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv_sock.settimeout(0.1)
        i = 1
        try:
            print("Main Thread: before accepting...")
            while True:
                
                try:
                    
                    c,a = srv_sock.accept()
                    t = threading.Thread(target=self.handle_client,args=(c,a,str(i)))
                    t.start()
                    i += 1
                    threads.append(t)
                    if all_to_die:
                        break
                    if i > 1000:
                        print("Server going down")
                        break
                except socket.timeout:
                    if all_to_die:
                        break
                
            all_to_die = True
            print("Main Thread: waiting for all client to die")
            for t in threads:
                t.join()
        finally:
            srv_sock.close()
            print("Bye..")
    
    
    def found_answer(self,answer:int):
        print("\n" + " " * 10 + "#######################################")
        print(" " * 10 +"       ANSWER is " + str(answer).zfill(10))
        print(" " * 10 + "#######################################")
        print(" " * 10 + f"finding answer took {self.tend - self.tstart}s using {len(self.clients)} computers.")
        print("\n")
    
    def _exit(self):
        global all_to_die
        print("Exiting...")
        for clinet in self.clients:
            send_data(b"EXIT",clinet.get_sock(),log=False)
        all_to_die = True
        exit()


if __name__ == "__main__":
    
    server = Server()
    server.main()