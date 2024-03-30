import socket, threading, traceback,time
import os 
import traceback,smtplib,ssl,random


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from email.message import EmailMessage

from hashlib import sha256


from users import UsersDict
from aes_helper import AES_encrypt,AES_decrypt





#fixed variables

USERS = UsersDict()

PEPPER = "neverhackme"

SENDER_EMAIL = 'verify.idan.python@gmail.com'
SENDER_PASSWORD = "heeu zvaf jjgp vjnv"





def logtcp(dir, byte_data,):
    """
    Log direction, tid, and all TCP byte array data.
    Return: void
    """
    if dir == 'sent':
        print(f'S LOG:Sent     >>> {byte_data}')
    else:
        print(f'S LOG:Recieved <<< {byte_data}')


def send_data(sock, tid, bdata,key):
    """
    send to client byte array data
    will add 8 bytes message length as first field
    e.g. from 'abcd' will send  b'00000004~abcd'
    return: void
    """
    #encryps data with AES
    #it sends first the iv and then the encrypted data

    
    if len(bdata) == 0:
        sock.send(b'')
        return
        
    iv, ciphertext = AES_encrypt(key,bdata)
    bytearray_data: bytes = str(len(ciphertext)).zfill(8).encode() + b'~' + ciphertext
    to_send :bytes = iv + b'|' + bytearray_data
    sock.send(to_send)
    logtcp('sent', to_send)


def recive_by_size(sock:socket, key:bytes) -> str:
    """recive msg with sockets, using the first 8 bytes as the size of the msg and decrypting it with AES
    the message is in the format of 'iv|size~encrypted_msg'


    Returns:
        str: the mesesage itself (without the iv and the size)
    """
    #this will also decrypt the data with AES
    
    # sock.settimeout(3)
    
    iv = sock.recv(16)
    if iv == b'' :#clinet disconnected
        return ''
    
    #in case not all the data wax recieved at once
    while not b'|' in iv:
        iv += sock.recv(4)
    #will probably recive more than just the iv
    parts = iv.split(b'|')
    iv = parts[0]
    
    #the rest of the recived data belongs to the size
    size = parts[1]
    while not b'~' in size:
        size += sock.recv(4)
    
    parts = size.split(b'~')
    size = int(parts[0].decode())
    
    enc_msg = parts[1]
    while len(enc_msg) != size:
        
        enc_msg += sock.recv(size)
    
    msg = AES_decrypt(key,iv,enc_msg)
    logtcp('recv',msg)
    
    #after we got both the msg and the iv we can decrypt the data
    return msg.decode()


def _hash(data):
    """
    Hash the data.
    Return: string - hashed data
    """
    return sha256(data.encode()).hexdigest()

def _salt() -> str:
    return os.urandom(4).hex()


def send_email_verification(email_reciver: str,code:str) -> str:
        
        #send user an email with a verification code and return the code

        em = EmailMessage()
        em['from'] = SENDER_EMAIL
        em['to'] = email_reciver
        em['subject'] = 'verification'


        em.set_content(f'your verification code is '+ code)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(SENDER_EMAIL,SENDER_PASSWORD)
            smtp.sendmail(SENDER_EMAIL,email_reciver,em.as_string())
            print('sent')
            
        return code   




def generate_keys():
    """
    generates keys for RSA
    
    returns:
    tuple(private_key, public_key)
    """
    
    
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

#RSA
def AES_key_exchange(sock:socket) -> bytes:
    """
    swaps with clinet keys for AES using RSA
    first the server sends public key, than clinet sends AES key encrypted using the public key, than server decrypts the AES key. Handshake done
    

    Args:
        sock (socket): the socket

    Returns:
        bytes: AES key
    """
    
    private_key, public_key = generate_keys()
    sock.send(public_key)
    


    
    enc_key = sock.recv(1024)

    AES_key = PKCS1_OAEP.new(RSA.import_key(private_key)).decrypt(enc_key)
    
    print("Received key:", AES_key)
    return AES_key
    
    


def handle_request(data):
    finish = False
    fields: list[bytes] = data.split(b'~')
    command = fields[0]
    to_send = b''
    if command == b'sign_in':
        salt = USERS.get_salt(fields[1].decode())
        to_send = USERS.check_sign_in(fields[1].decode(), _hash(fields[2].decode() + salt + PEPPER))
    elif command == b'sign_up':
        code = str(random.randint(0,9999)).zfill(4) #create a varification code
        salt = _salt() #create a new salt
        to_send = USERS.sign_up(fields[1].decode(), _hash(fields[2].decode() + salt + PEPPER),_hash(fields[3].decode() + salt + PEPPER),salt,code)
        #info is valid
        if to_send == 'ack':
            send_email_verification(fields[1].decode(),code)
            to_send = 'code~' + fields[1].decode() + '~' + code
    elif command == b'ack':
        to_send = USERS.ack_user(fields[1].decode())
    
        
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
    
    key = AES_key_exchange(sock)
    
    
    
    while not finish:
        if all_to_die:
            print('will close due to main server issue')
            break
        try:
            byte_data = recive_by_size(sock,key).encode()  
            if byte_data == b'':
                print('Seems client disconnected')
                break

            err_size = b''
            if err_size != b'':
                to_send = err_size
            else:
                to_send, finish = handle_request(byte_data)
            if to_send != '':
                send_data(sock, tid, to_send.encode(),key)
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