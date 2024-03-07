import json,threading,os

class UsersDict:
    users: dict = {}
    lock = threading.Lock()
    
    def __init__(self) -> None:
        self.users = load_users()
    
    def does_user_exists(self,user: str) -> bool:
        return user in self.users.keys()
    
    def check_sign_in(self,username, password) -> str:
        with self.lock:
            if self.does_user_exists(username):
                if self.users[username] == password:
                    to_send = "ack"
                else:
                    to_send = "err~wrong password"
            else:
                to_send = "err~Username not found"
        return to_send

    def sign_up(self,username, password, cpassword) -> str:
        with self.lock:
            if self.does_user_exists(username):
                to_send = "err~username already exists"
            elif password != cpassword:
                to_send = "err~passwords aren't identical"
            else:
                self.users[username] = password
                to_send = "ack"
        return to_send

    def save_data(self):
        
        json.dump(self.users, open('users.json', 'w'))



    def clear(self):
        os.remove(r"w:\RETyk\gui_cli_n_ser\users.json")
    

def load_users() -> dict:
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except:
        return {}


