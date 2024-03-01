import tkinter as tk
from tkinter import ttk

import socket,traceback


class GUI():
    def send_sign_in(self):
        self.to_send = f"in~{self.username}~{self.password}"
        self.root.destroy()

    def sign_in(self):
        self.root = tk.Tk()
        self.root.geometry("450x300")
        self.root.title("sign in")
        self.mainframe = tk.Frame(self.root,background="white")
        self.mainframe.pack(fill="both",expand=True)


        text = ttk.Label(self.mainframe,text="Email Address:",background="white",font=("Brass Mono",10),)
        text.grid(row=0,column=0)

        self.username = ttk.Entry(self.mainframe)
        self.username.grid(row =1, column=0,sticky="NWES")

        text = ttk.Label(self.mainframe,text="Password:",background="white",font=("Brass Mono",10),)
        text.grid(row=3,column=0)
        
        self.password = ttk.Entry(self.mainframe,show='*')
        self.password.grid(row =4, column=0,sticky="NWES")

        
        login = ttk.Button(self.mainframe,text="LOGIN",command=self.send_sign_in)
        login.grid(row=6,column=1)

        self.root.mainloop()

    
        return self.to_send
    
    def send_sign_up(self):
        self.to_send = f"up~{self.username}~{self.password}"
        self.root.destroy()
    
    def sign_up(self):
        self.root = tk.Tk()
        self.root.geometry("450x300")
        self.root.title("sign in")
        self.mainframe = tk.Frame(self.root,background="white")
        self.mainframe.pack(fill="both",expand=True)

        #email
        text = ttk.Label(self.mainframe,text="Email Address:",background="white",font=("Brass Mono",10),)
        text.grid(row=0,column=0)

        self.username = ttk.Entry(self.mainframe)
        self.username.grid(row =1, column=0,sticky="NWES")

        #ps
        text = ttk.Label(self.mainframe,text="Password:",background="white",font=("Brass Mono",10),)
        text.grid(row=3,column=0)
        
        self.password = ttk.Entry(self.mainframe,show='*')
        self.password.grid(row =4, column=0,sticky="NWES")

        #confrim ps
        text = ttk.Label(self.mainframe,text="Confirm Password:",background="white",font=("Brass Mono",10),)
        text.grid(row=5,column=0)
        
        self.password = ttk.Entry(self.mainframe,show='*')
        self.password.grid(row =4, column=0,sticky="NWES")
        
        createAcc = ttk.Button(self.mainframe,text="Create Account",command=self.check_login)
        createAcc.grid(row=6,column=1)

        self.root.mainloop()


        return self.to_send
    
    

    def show_menu(self):
        self.root = tk.Tk()
        self.root.geometry("450x300")
        sign_in = ttk.Button(self.mainframe,text="I already have an account",command = self.sign_in())
        sign_in.grid(row=2,column=3)
        sign_up = ttk.Button(self.mainframe,text="Create new account",command=self.sign_up())
        sign_up.grid(row=2,column=5)
        
        



def logtcp(dir, byte_data):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{byte_data}')
    else:
        print(f'C LOG:Recieved <<<{byte_data}')


def send_data(sock, bdata):
    """
    send to client byte array data
    will add 8 bytes message length as first field
    e.g. from 'abcd' will send  b'00000004~abcd'
    return: void
    """
    bytearray_data = str(len(bdata)).zfill(8).encode() + b'~' + bdata
    sock.send(bytearray_data)
    logtcp('sent', bytearray_data)


def menu():
    """
    show client menu
    return: string with selection
    """
    print('\n  1. take screenshot')
    print('\n  2. send file')
    print('\n  3. display directory')
    print('\n  4. delete file ')
    print('\n  5. copy file ')
    print('\n  6. run executeable file')
    print('\n  7. notify exit')
    print('\n  (8. some invalid data for testing)')
    return input(' which action do you want? (1-8) ' )


def protocol_build_request(from_user):
    """
    build the request according to user selection and protocol
    return: string - msg code
    """
    if from_user == '1':
        return 'SCRN~' + input ('enter name the screen shot will be saved ')
    elif from_user == '2':
        return 'SNDF~' + input('enter file absolute or relative path ')
    elif from_user == '3':
        return 'DIRS~' + input('enter directory absolute or relative path ')
    elif from_user == '4':
        return 'DELF~' + input('enter file absolute or relative path ')
    elif from_user == '5':
        pathFrom = input('enter file current location path')
        pathTo = input('enter file copy location path')
        return 'COPF~' + pathFrom + '~' + pathTo 
    elif from_user == '6':
        return 'RUNF~' + input('enter file absolute or relatvie path ')
    elif from_user == '7':
        return 'EXIT'
    elif from_user == '8':
        return input("enter free text data to send> ")
    else:
        return ''


def protocol_parse_reply(reply):
    """
    parse the server reply and prepare it to user
    return: answer from server string
    """
   
    
    
    pass


def handle_reply(reply): #reply is the message without the length field
    """
    get the tcp upcoming message and show reply information
    return: void
    """
    to_show = protocol_parse_reply(reply)
    if to_show != '':
        print('\n==========================================================')
        print (f'  SERVER Reply: {to_show}   |')
        print(  '==========================================================')





def recive_by_size(sock):
    
    size = ''
    while not size.__contains__('~'):
        size += sock.recv(4).decode()
    parts = size.split('~')
    size = int(parts[0])
    
    msg = parts[1]
    while len(msg) != size:
        
        msg += sock.recv(size).decode()
    logtcp('recv',msg)
    return msg



def main(ip):
    """
    main client - handle socket and main loop
    """
    connected = False

    sock= socket.socket()

    port = 1233
    try:
        sock.connect((ip,port))
        print (f'Connect succeeded {ip}:{port}')
        connected = True
    except:
        print(f'Error while trying to connect.  Check ip or port -- {ip}:{port}')

    while connected:
        to_send = GUI().show_menu()
        if to_send =='':
            print("Selection error try again")
            continue
        try :
            send_data(sock,to_send.encode())
            byte_data = recive_by_size(sock)   
            if byte_data == b'':
                print ('Seems server disconnected abnormal')
                break
           
            
            
            
            print(byte_data.decode())

            
        except socket.error as err:
            print(f'Got socket error: {err}')
            break
        except Exception as err:
            print(f'General error: {err}')
            print(traceback.format_exc())
            break
    print ('Bye')
    sock.close()


if __name__ == '__main__':
    main("127.0.0.1")