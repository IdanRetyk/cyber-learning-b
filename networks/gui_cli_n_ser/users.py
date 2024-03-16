import json,threading,os,re


import smtplib,ssl,random

from email.message import EmailMessage

SENDER_EMAIL = 'verify.idan.ipython@gmail.com'
SENDER_PASSWORD = 'Python123!'
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
    return re.match(r"^[A-Za-z_0-9]+@[A-Za-z_0-9]+.[A-Za-z_0-9]+",email) is not None
    
    



def send_email_verification(email_reciver: str) -> str:
        
        #send user an email with a verification code and return the code

        em = EmailMessage()
        em['from'] = SENDER_EMAIL
        em['to'] = email_reciver
        em['subject'] = 'verification'

        code = str(random.randint(0,9999)).zfill(4)
        em.set_content(f'your verification code is '+ code)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(SENDER_EMAIL,SENDER_PASSWORD)
            smtp.sendmail(SENDER_EMAIL,email_reciver,em.as_string())
            print('sent')
            
        return code   