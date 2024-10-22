import socket,threading
import traceback
from networking_helper import *


class Chunk():
    count: int = 0
    def __init__(self,range: tuple[int,int]) -> None:
        self.__id = Chunk.count
        self.__range = range
        self.__done: bool = False
        Chunk.count += 1
    
    def get_range(self) -> tuple[int,int]:
        return self.__range
    
    def get_id(self) -> int:
        return self.__id
    
    def if_done(self) -> bool:
        return self.__done
    
    def make_done(self):
        self.__done = True


class Client_info():
    def __init__(self,sock: socket.socket,cpu_count: int) -> None:
        self.__sock = sock
        self.__cpu_count = cpu_count
    
    def get_sock(self) -> socket.socket:
        return self.__sock

    def set_sock(self, sock: socket.socket):
        self.__sock = sock

    def get_cpu_count(self) -> int:
        return self.__cpu_count

    def set_cpu_count(self, cpu_count: int):
        self.__cpu_count = cpu_count

class Server():
    def __init__(self) -> None:
        self.chunks = self.get_chunks()
        self.clients :list[Client_info] = [] # {<tid>:<socket>}
        
    
    def get_chunks(self) -> list[Chunk]:
        chunks: list[Chunk] = []
        for i in range(100):
            chunks.append(Chunk((10_000_00 * i,10_000_000 * (i + 1))))
            
        return chunks

    def get_next_chunk(self) -> Chunk:
        for chunk in self.chunks:
            if not chunk.if_done():
                return chunk
        self._exit()
        return self.chunks[0]


    def handshake(self,sock: socket.socket,tid: int) -> bool:
        data = recv_by_size(sock).split(b'~')
        if not data:
            return True
        _,cpu_count = data
        cpu_count = int(cpu_count)
        self.clients[tid] = Client_info(sock,cpu_count)
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
        match command:
            case "DONE":
                # message consists of every chunk that client has finished.
                for chunk_id in fields[1:]:
                    self.chunks[int(chunk_id)].make_done()
                for _ in self.clients[tid].get_cpu_count():
                    chunk = self.get_next_chunk()
                    start,end = chunk.get_range()
                    to_send += f'NEW~{start}~{end}~{chunk.get_id()}!'.encode()
                    
            case "FOUND":
                answer = int(fields[1])
                self.found_answer(answer)
                to_send = b'ack'
                self._exit()
            case _:
                to_send = b'Unknown command'
        
        return to_send,finish


    def handle_client(self,sock: socket.socket,addr: socket._Address, tid: str):
        global all_to_die
        
        finish = False
        print(f"New client number {tid} from {addr}")
        finish = self.handshake(sock,int(tid))
        while not finish:
            if all_to_die:
                print("Closing client due to server issue")
                all_to_die = True
                break
            try:
                bdata: bytes = recv_by_size(sock)
                if not bdata:
                    print(f"Client {tid} disconnected")
                    finish = True
                    break
                logtcp("recv",bdata,tid)
                to_send,finish = self.handle_request(bdata,int(tid))
                if finish:
                    break
                if to_send:
                    send_data(to_send,sock,tid)
                
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
        
        i = 1
        while True:
            print("Main Thread: before accepting...")
            c,a = srv_sock.accept()
            t = threading.Thread(target=self.handle_client,args=(c,a,str(i)))
            t.start()
            i += 1
            threads.append(t)
            if i > 1000:
                print("Sever going down")
                break
            
        all_to_die = True
        print("Main Thread: waiting for all client to die")
        for t in threads:
            t.join()
        srv_sock.close()
        print("Bye..")
    
    
    def found_answer(self,answer:int):
        print("FOUND ANSWER - " + str(answer))
    
    
    def _exit(self):
        print("Exiting...")
        for clinet in self.clients:
            send_data(b"EXIT",clinet.get_sock())


if __name__ == "__main__":
    
    server = Server()
    server.main()