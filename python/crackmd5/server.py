import socket,threading
import traceback

from networking_helper import *


def handle_request(data :bytes) -> tuple[bytes,bool]:
    return b'',True


def handle_client(sock: socket.socket,addr: socket._Address, tid: str):
    global all_to_die
    
    finish = False
    print(f"New client number {tid} from {addr}")
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
            logtcp("recv",tid,bdata)
            to_send,finish = handle_request(bdata)
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



def main():
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
        t = threading.Thread(target=handle_client,args=(c,a,str(i)))
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


if __name__ == "__main__":
    main()