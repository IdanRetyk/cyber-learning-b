import tkinter as tk
from tkinter import ttk

import socket,traceback,smtplib,ssl,random

from email.message import EmailMessage


SENDER_EMAIL = 'verify.idan.python@gmail.com'
SENDER_PASSWORD = "heeu zvaf jjgp vjnv"

class GUI():
    

    
    def send_sign_in(self):
        self.to_send = f"sign_in~{self.username.get()}~{self.password.get()}"
        self.rootSI.destroy()
        try:
            self.root.destroy()
        except:
            pass

    def sign_in(self, error = ""):
        self.rootSI = tk.Tk()
        self.rootSI.geometry("450x300+500+400")
        self.rootSI.title("sign in")
        self.mainframeSI = tk.Frame(self.rootSI,background="white")
        self.mainframeSI.pack(fill="both",expand=True)


        text = ttk.Label(self.mainframeSI,text="Email Address:",background="white",font=("Brass Mono",10),)
        text.grid(row=0,column=0)

        self.username = ttk.Entry(self.mainframeSI)
        self.username.grid(row =1, column=0,sticky="NWES")

        text = ttk.Label(self.mainframeSI,text="Password:",background="white",font=("Brass Mono",10),)
        text.grid(row=3,column=0)
        
        self.password = ttk.Entry(self.mainframeSI,show='*')
        self.password.grid(row =4, column=0,sticky="NWES")

        
        error = ttk.Label(self.mainframeSI,text=error,background = "white",foreground = "red")
        error.grid(row = 10,column=0)
        
        
        
        login = ttk.Button(self.mainframeSI,text="LOGIN",command=self.send_sign_in)
        login.grid(row=6,column=1)

        self.rootSI.mainloop()

        
        return self.to_send
    
    def send_sign_up(self):
        self.to_send = f"sign_up~{self.username.get()}~{self.password.get()}~{self.Cpassword.get()}"
        self.rootSU.destroy()
        try:
            self.root.destroy()
        except:
            pass
    
    def sign_up(self,error = ""):
        self.rootSU = tk.Tk()
        self.rootSU.geometry("450x300+500+400")
        self.rootSU.title("sign in")
        self.mainframeSU = tk.Frame(self.rootSU,background="white")
        self.mainframeSU.pack(fill="both",expand=True)

        #email
        text = ttk.Label(self.mainframeSU,text="Email Address:",background="white",font=("Brass Mono",10),)
        text.grid(row=0,column=0)

        self.username = ttk.Entry(self.mainframeSU)
        self.username.grid(row =1, column=0,sticky="NWES")

        #ps
        text = ttk.Label(self.mainframeSU,text="Password:",background="white",font=("Brass Mono",10),)
        text.grid(row=3,column=0)
        
        self.password = ttk.Entry(self.mainframeSU,show='*')
        self.password.grid(row =4, column=0,sticky="NWES")

        #confrim ps
        text = ttk.Label(self.mainframeSU,text="Confirm Password:",background="white",font=("Brass Mono",10),)
        text.grid(row=5,column=0)
        
        self.Cpassword = ttk.Entry(self.mainframeSU,show='*')
        self.Cpassword.grid(row =7, column=0,sticky="NWES")
        
        createAcc = ttk.Button(self.mainframeSU,text="Create Account",command=self.send_sign_up)
        createAcc.grid(row=8,column=1)

        error = ttk.Label(self.mainframeSU,text=error,background = "white",foreground = "red")
        error.grid(row = 10,column=0)
        
        
        
        self.rootSU.mainloop()

        
        return self.to_send
        
    

    def show_menu(self):
        self.root = tk.Tk()
        self.root.geometry("450x300+500+400")
        self.root.title("Choose your opntion")
        self.mainframe = tk.Frame(self.root,background="white")
        self.mainframe.pack(fill="both",expand=True)
        self.to_send = ''
        
        sign_in = ttk.Button(self.mainframe,text="I already have an account",command = self.sign_in)
        sign_in.grid(row=0,column=0)
        sign_up = ttk.Button(self.mainframe,text="Create new account",command=self.sign_up)
        sign_up.grid(row=2,column=5)
        
        
        close = ttk.Button(self.mainframe,text="Close",command = lambda : self.root.destroy())
        close.grid(row=0,column=6)
        
        self.root.mainloop()
        return self.to_send
        
        
        
        
    def ack_window(self):
        ack_root = tk.Tk()
        ack_root.geometry("250x80+400+300")
        ack_root.title("Acknoledgment Window")
        ack_mainframe = tk.Frame(ack_root,background="white")
        ack_mainframe.pack(fill="both",expand=True)
        ack = ttk.Label(ack_mainframe,text="Action was done succesfuly!",background="white",font=("Brass Mono",10),justify="center")
        ack.grid(row=0,column=0)
        
        close = ttk.Button(ack_mainframe,text="Close",command = lambda : ack_root.destroy())
        close.grid(row=1,column=0)
        
        ack_root.mainloop()
        
        
    
    def ver_window(self,display_wrong = False):
        self.ver_root = tk.Tk()
        self.ver_root.geometry("500x80+500+400")
        self.ver_root.title("Verification Window")
        ver_mainframe = tk.Frame(self.ver_root,background="white")
        ver_mainframe.pack(fill="both",expand=True)
        ver = ttk.Label(ver_mainframe,text="Please enter the verification code sent to your email",background="white",font=("Brass Mono",10),justify="center")
        ver.grid(row=0,column=0)
        
        self.ver_code: ttk.Entry = ttk.Entry(ver_mainframe)
        self.ver_code.grid(row = 1, column = 0,sticky="NWES")
        
        
        if display_wrong:
            wrong = ttk.Label(ver_mainframe,text="Wrong code, please try again",background="white",font=("Brass Mono",10),justify="center",foreground="red")
            wrong.grid(row=3,column=0)
        
        close = ttk.Button(ver_mainframe,text="Done",command = self.get_code)
        close.grid(row=2,column=0)
        
        self.ver_root.mainloop()
        

        return self.code
        
    def get_code(self):
        self.code = self.ver_code.get()
        self.ver_root.destroy() 




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
    if len(bdata) == 0:
        sock.send(b'')
    else:
        bytearray_data = str(len(bdata)).zfill(8).encode() + b'~' + bdata
        sock.send(bytearray_data)
        logtcp('sent', bytearray_data)




def parse_error(data,gui: GUI):
    fields = data.split('~')
   
    to_send = ""

    #handle wrong user input
    error_msg = fields[2]
    if fields[1] == "1":
        #errors in sign up
        to_send = gui.sign_up(error_msg)
    elif fields[1] == "2":
        #error in sign in
        to_send = gui.sign_in(error_msg)

    return to_send.encode()

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

    if (connected):
        gui = GUI()
        to_send = gui.show_menu()
        print (f"to send {to_send} ")
        if to_send =='':
            print("Selection error try again")
            
        try :
            send_data(sock,to_send.encode())
            data = recive_by_size(sock)
            command = data.split('~')[0] 
            if data == '':
                print ('Seems server disconnected abnormal')
            
            while command == 'err':
                send_data(sock,parse_error(data,gui))
                data = recive_by_size(sock)
                command = data.split('~')[0] 
            

            if command == 'code':
                print("now we should recivece code")
                correct_code = data.split('~')[2]
                code = gui.ver_window()
                while(correct_code != code):
                    code = gui.ver_window(True)
                send_data(sock,f"ack~{data.split('~')[1]}".encode())
                                  
                
                
            while command == 'err':
                send_data(sock,parse_error(data,gui))
                data = recive_by_size(sock)
                command = data.split('~')[0] 
           
            
            print(data, type(data))

            
        except socket.error as err:
            print(f'Got socket error: {err}')
            
        except Exception as err:
            print(f'General error: {err}')
            print(traceback.format_exc())
    gui.ack_window()
    print ('Bye')
    sock.close()


if __name__ == '__main__':
    main("127.0.0.1")