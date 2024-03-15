import json,threading,os,re





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
            # elif not is_valid(username):
            #     to_send = "err~2~Please enter a valid email!"
            else:
                to_send = "ack"
        return to_send

    def get_salt(self,username) -> str:
        try:
            return self.users[username][1]
        except:
            pass 
    
    def sign_up(self,username, password, cpassword,salt) -> str:
        with self.lock:
            
            #check for errors
            if self.does_user_exists(username):
                to_send = "err~1~username already exists"
            elif password != cpassword:
                to_send = "err~1~passwords aren't identical"
            
            #actually sign up
            else:
                self.users[username] = password,salt
                to_send = "ack"
        
        
        return to_send

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
    return re.match(r"(a-zA-Z0-9._%+-]+@(a-zA-Z0-9._%+-])+(\.(a-zA-Z0-9._%+-]+)+$",email) is not None
    
    



