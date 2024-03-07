import socket, threading, traceback,time

from users import UsersDict
from hashlib import sha256

USERS = UsersDict()


def logtcp(dir, tid, byte_data):
    """
    Log direction, tid, and all TCP byte array data.
    Return: void
    """
    if dir == 'sent':
        print(f'{tid} S LOG:Sent     >>> {byte_data}')
    else:
        print(f'{tid} S LOG:Recieved <<< {byte_data}')


def send_data(sock, tid, bdata):
    """
    Send to client byte array data.
    Will add 8 bytes message length as the first field.
    E.g., from 'abcd' will send b'00000004~abcd'.
    Return: void
    """
    bytearray_data = (str(len(bdata)).zfill(8) + '~' + bdata).encode()
    sock.send(bytearray_data)
    logtcp('sent', tid, bytearray_data)
    print("")


def check_length(message):
    """
    Check message length.
    Return: string - error message
    """
    return b''


def _hash(data):
    """
    Hash the data.
    Return: string - hashed data
    """
    return sha256(data.encode()).hexdigest()


def handle_request(data):
    finish = False
    fields = data.split(b'~')
    command = fields[0]
    to_send = b''
    if command == b'sign_in':
        to_send = USERS.check_sign_in(fields[1].decode(), _hash(fields[2].decode()))
    elif command == b'sign_up':
        to_send = USERS.sign_up(fields[1].decode(), _hash(fields[2].decode()),_hash(fields[3].decode()))
    else:
        print("unknown command")
        finish = True
    return to_send, finish


def handle_client(sock, tid, addr):
    """
    Main client thread loop (in the server),
    :param sock: client socket
    :param tid: thread number
    :param addr: client ip + reply port
    :return: void
    """
    global all_to_die
    all_to_die = False
    finish = False
    print(f'New Client number {tid} from {addr}')
    while not finish:
        if all_to_die:
            print('will close due to main server issue')
            break
        try:
            byte_data = sock.recv(1000)  # todo improve it to recv by message size
            if byte_data == b'':
                print('Seems client disconnected')
                break
            logtcp('recv', tid, byte_data)
            err_size = check_length(byte_data)
            if err_size != b'':
                to_send = err_size
            else:
                byte_data = byte_data[9:]  # remove length field
                to_send, finish = handle_request(byte_data)
            if to_send != '':
                send_data(sock, tid, to_send)
            if finish:
                time.sleep(1)
                break
        except socket.error as err:
            print(f'Socket Error exit client loop: err:  {err}')
            break
        except Exception as err:
            print(f'General Error %s exit client loop: {err}')
            print(traceback.format_exc())
            break
    USERS.save_data()
    print(f'Client {tid} Exit')
    sock.close()


def main():
    global all_to_die
    global USERS
    """
    Main server loop
    1. accept tcp connection
    2. create thread for each connected new client
    3. wait for all threads
    4. every X clients limit will exit
    """
    USERS = UsersDict()
    
    threads = []
    srv_sock = socket.socket()

    srv_sock.bind(('127.0.0.1', 1233))

    srv_sock.listen(20)

    # next line release the port
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    i = 1
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, str(i), addr))
        t.start()
        i += 1
        threads.append(t)
        if i > 100000000:  # for tests change it to 4
            print('\nMain thread: going down for maintenance')
            break

    all_to_die = True
    print('Main thread: waiting to all clients to die')
    for t in threads:
        t.join()
    srv_sock.close()
    USERS.save_data()
    print('Bye ..')


if __name__ == '__main__':
    main()
