import sqlite3

__author__ = 'user'

class Movie:
    def __init__(self, ID, title, director, rating, time):
        self.ID = ID
        self.title = title
        self.director = director
        self.rating = rating
        self.time = time

    def __str__(self):
        return f"{self.ID}~{self.title}~{self.director}~{self.rating}~{self.time}"

class Screen:
    def __init__(self, ID, movie_title, hour, is_vip):
        self.ID = ID
        self.movie_title = movie_title
        self.hour = hour
        self.is_vip = is_vip

class MovieScreenORM:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open_db(self):
        self.conn = sqlite3.connect('MovieScreen.db')
        self.cursor = self.conn.cursor()
        
    def close_db(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    # All read SQL
    def get_user(self, username):
        self.open_db()
        user = None
        # sql = "SELECT ................ "
        result = self.cursor.execute(sql)
        self.close_db()
        return user
    
    def get_users(self):
        self.open_db()
        users = []
        self.close_db()
        return users

    def get_user_balance(self, username):
        self.open_db()
        sql = f"SELECT a.Balance FROM Accounts a, Users b WHERE a.AccountID = b.AccountID AND b.Username = '{username}'"
        result = self.cursor.execute(sql)
        balance = result.fetchone()[0]
        self.close_db()
        return balance

    # All write SQL
    def withdraw_by_username(self, amount, username):
        pass

    def deposit_by_username(self, amount, username):
        pass

    def insert_new_user(self, username, password, firstname, lastname, address, phone, email, account_id):
        pass

    def insert_new_account(self, user):
        self.open_db()
        sql = "SELECT MAX(AccountID) FROM Accounts"
        result = self.cursor.execute(sql)
        account_id = result.fetchone()[0] + 1
        sql = (
            "INSERT INTO Users (Username, Password, Fname, Lname, Address, Phone, Email, AccountID, IsAdmin) "
            f"VALUES('{user.username}', '{user.password}', '{user.firstname}', '{user.lastname}', "
            f"'{user.address}', '{user.phone}', '{user.email}', {account_id}, 'no')"
        )
        self.cursor.execute(sql)
        sql = f"INSERT INTO Accounts (AccountID, Balance, Manager) VALUES({account_id}, 0, '{user.username}')"
        self.cursor.execute(sql)
        self.commit()
        self.close_db()
        return "Ok"

    def add_movie(self, movie):
        self.open_db()
        sql = (
            "INSERT INTO Movies (ID, Title, Director, Rating, Time) "
            f"VALUES('{movie.ID}', '{movie.title}', '{movie.director}', '{movie.rating}', '{movie.time}')"
        )
        self.cursor.execute(sql)
        self.commit()
        self.close_db()
        return "Ok"

    def get_movies_at_hour(self, hour):
        self.open_db()
        sql = f"SELECT * FROM Movies WHERE Time = '{hour}'"
        result = self.cursor.execute(sql)
        movies = result.fetchall()
        self.close_db()
        return movies

    def get_best_rated_movies(self, amount):
        self.open_db()
        sql = f"SELECT * FROM Movies ORDER BY Rating DESC LIMIT {amount}"
        result = self.cursor.execute(sql)
        movies = result.fetchall()
        self.close_db()
        return movies

    def get_vip_movies(self):
        self.open_db()
        sql = "SELECT MovieTitle, Hour FROM Screen WHERE IsVIP = 1"
        result = self.cursor.execute(sql)
        movies = result.fetchall()
        self.close_db()
        return movies

    def add_screen(self, screen):
        self.open_db()
        sql = (
            "INSERT INTO Screen (ID, MovieTitle, Hour, IsVIP) "
            f"VALUES ({screen.ID}, '{screen.movie_title}', '{screen.hour}', {screen.is_vip})"
        )
        self.cursor.execute(sql)
        self.commit()
        self.close_db()
        return True

    def make_vip(self, screen_id):
        self.open_db()
        sql = f"SELECT * FROM Screen WHERE ID = {screen_id}"
        result = self.cursor.execute(sql)
        if not result.fetchall():
            self.close_db()
            return "dont_exist"
        sql = f"UPDATE Screen SET IsVIP = 1 WHERE ID = {screen_id}"
        self.cursor.execute(sql)
        self.commit()
        self.close_db()
        return True

    def delete_user(self, username):
        pass

    def delete_account(self, account_id):
        pass

    def get_all_movies(self):
        self.open_db()
        sql = "SELECT * FROM Movies"
        result = self.cursor.execute(sql)
        movies = result.fetchall()
        self.close_db()
        return movies

def main_test():
    movie1 = Movie("1234", "Example Title", "Example Director", "10", "16:00")
    db = MovieScreenORM()
    db.add_movie(movie1)
    movies = db.get_all_movies()
    for movie in movies:
        print(movie)

if __name__ == "__main__":
    main_test()
