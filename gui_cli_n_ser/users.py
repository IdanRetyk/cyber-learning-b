import pickle,threading

class UsersDict:
    users: dict = {}
    lock = threading.Lock()
    
    def __init__(self,data: dict = {}) -> None:
        self.users = data
    
    def does_user_exists(self,user: str) -> bool:
        return user in self.users.keys()
    
    def check_sign_in(self,username, password) -> str:
        with self.lock:
            if self.does_user_exists(username):
                if self.users[username] == password:
                    to_send = "ack"
                else:
                    to_send = "wrong password"
            else:
                to_send = "Username not found"
        return to_send

    def sign_up(self,username, password) -> str:
        with self.lock:
            if self.does_user_exists(username):
                to_send = "username already exists"
            else:
                self.users[username] = password
                to_send = "ack"
        return to_send

    def save_data(self):
        pickle.dump(self.users, open('users.pkl', 'wb'))


def load_users() -> dict:
    try:
        with open('users.pkl', 'rb') as file:
            return pickle.load(file)
    except:
        return {}


def dump_users(data) -> None:
    pickle.dump(data, open('users.pkl', 'wb'))