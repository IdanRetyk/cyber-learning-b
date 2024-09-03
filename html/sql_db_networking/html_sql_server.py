__author__ = 'Yossi'

import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
import SQL_ORM

DEBUG = True
exit_all = False

def handle_client(sock, client_id, db):
    global exit_all
    
    print(f"New client connected: {client_id}")
    
    while not exit_all:
        try:
            data = recv_by_size(sock)
            if not data:
                print("Error: Client disconnected")
                break

            data = data.decode()
            response = process_action(data, db)
            
            send_with_size(sock, response)

        except socket.error as err:
            if err.errno == 10054:
                print(f"Error {err.errno}: Client {sock} reset by peer.")
                break
            else:
                print(f"Error {err.errno}: General socket error. Client {sock} disconnected.")
                break

        except Exception as err:
            print("General Error:", err)
            break

    sock.close()

def process_action(data, db):
    action = data[:9]  # Adjusted to match the longer action names
    data = data[10:]
    fields = data.split('|')
    response = "Not Set Yet"

    if DEBUG:
        print(f"Received client request: {action} -- {fields}")

    if action == "ADD_MOVIE":
        movie = SQL_ORM.Movie(fields[0], fields[1], fields[2], fields[3], fields[4])
        if db.add_movie(movie) == "Ok":
            response = "ADD_MOVIE|Success"
        else:
            response = "ADD_MOVIE|Error"
    
    elif action == "MOVIES_AT_TIME":
        hour = fields[0]
        movies = db.get_movies_at_hour(hour)
        movies_str = ''.join([str(movie) for movie in movies])
        response = f"MOVIES_AT_TIME|{movies_str}"

    elif action == "BEST_RATED_MOVIES":
        limit = fields[0]
        movies = db.get_best_rated_movies(limit)
        movies_str = ''.join([str(movie) for movie in movies])
        response = f"BEST_RATED_MOVIES|{movies_str}"

    elif action == "GET_ALL_MOVIES":
        movies = db.get_all_movies()
        movies_str = ''.join([str(movie) for movie in movies])
        response = f"GET_ALL_MOVIES|{movies_str}"

    elif action == "ADD_SCREEN":
        screen = SQL_ORM.Screen(fields[0], fields[1], fields[2], 0)
        if db.add_screen(screen):
            response = "ADD_SCREEN|Success"
        else:
            response = "ADD_SCREEN|Fail"

    elif action == "VIP_MOVIES":
        movies = db.get_vip_movies()
        movies_str = '~'.join([f"{movie[0]},{movie[1]}" for movie in movies])
        response = f"VIP_MOVIES|{movies_str}"

    elif action == "MAKE_VIP":
        screen_id = fields[0]
        result = db.make_vip(screen_id)
        if result == "dont_exist":
            response = "MAKE_VIP|Error|Screen ID does not exist"
        elif result:
            response = "MAKE_VIP|Success"

    elif action == "CHECK_LIVE":
        response = "CHECK_LIVE|Yes, I am a live server"

    else:
        print(f"Unknown action from client: {action}")
        response = f"ERROR|001|Unknown action: {action}"

    return response


def main():
    global exit_all
    
    db = SQL_ORM.MovieScreenORM()
    server_socket = socket.socket()
    
    server_socket.bind(("0.0.0.0", 33445))
    server_socket.listen(4)
    print("Server is listening...")

    threads = []
    client_id = 1

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id, db))
        client_thread.start()
        client_id += 1
        threads.append(client_thread)

    exit_all = True
    for t in threads:
        t.join()

    server_socket.close()

if __name__ == "__main__":
    main()
