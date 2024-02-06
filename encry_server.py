import tkinter as tk
from tkinter import ttk

class GUI():
    def check_login(self):
        
        print(self.username.get())
        print(self.password.get())

    def __init__(self):
        root = tk.Tk()
        root.geometry("450x300")
        root.title("sign in")
        mainframe = tk.Frame(root,background="white")
        mainframe.pack(fill="both",expand=True)


        text = ttk.Label(mainframe,text="Email Address:",background="white",font=("Brass Mono",10),)
        text.grid(row=0,column=0)

        self.username = ttk.Entry(mainframe)
        self.username.grid(row =1, column=0,sticky="NWES")

        text = ttk.Label(mainframe,text="Password:",background="white",font=("Brass Mono",10),)
        text.grid(row=3,column=0)
        
        self.password = ttk.Entry(mainframe)
        self.password.grid(row =4, column=0,sticky="NWES")

        
        login = ttk.Button(mainframe,text="LOGIN",command=self.check_login)
        login.grid(row=6,column=1)

        root.mainloop()


GUI()


