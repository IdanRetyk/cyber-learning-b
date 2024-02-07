import tkinter as tk
from tkinter import ttk
import socket


class GUI():
    def check_login(self):
        
        print(self.username.get())
        print(self.password.get())
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
        
        self.password = ttk.Entry(self.mainframe)
        self.password.grid(row =4, column=0,sticky="NWES")

        
        login = ttk.Button(self.mainframe,text="LOGIN",command=self.check_login)
        login.grid(row=6,column=1)

        self.root.mainloop()
