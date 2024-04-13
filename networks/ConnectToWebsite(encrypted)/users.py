import json,threading,os,re

import smtplib,ssl,random

from email.message import EmailMessage



class UsersDict:
    users: dict = {}
    lock = threading.Lock()
    
    def __init__(self) -> None:
        self.users = load_users()
    
    def does_user_exists(self,user: str) -> bool:
        return user in self.users.keys()
    
    def check_sign_in(self,username, password,) -> str:
        with self.lock:
            if not self.does_user_exists(username):
                to_send = "err~2~Username not found"
            elif not self.users[username][0] == password:
                to_send = "err~2~wrong password"
            
            else:
                to_send = "ack"
        return to_send

    def get_salt(self,username) -> str:
        try:
            return self.users[username][1]
        except:
            return "salt" #if user doesn't exist it doesn't matter what we return, when trying to log in it will fail anyway
    
    def sign_up(self,username, password, cpassword,salt,code) -> str:
        with self.lock:
            
            #check for errors
            if self.does_user_exists(username):
                to_send = "err~1~username already exists"
            elif password != cpassword:
                to_send = "err~1~passwords aren't identical"
            elif not is_valid(username):
                to_send = "err~1~Please enter a valid email!"
            
            #actually sign up
            else:
                self.users[username] = password,salt,code
                to_send = "ack"
        
        
        return to_send

    
    def ack_user(self,username):
        #remove the code from the database
        with self.lock:
            self.users[username] = self.users[username][0],self.users[username][1]
            return "ack"
        
        
    def save_data(self):
        
        json.dump(self.users, open('users.json', 'w'))



    def clear(self):
        os.remove("users.json")
    




def load_users() -> dict:
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except:
        return {}


def is_valid(email) -> bool:
    return re.match(r"^[A-Za-z_0-9\.]+@[A-Za-z_0-9\.]+\.[A-Za-z_0-9]+",email) is not None
    
    


