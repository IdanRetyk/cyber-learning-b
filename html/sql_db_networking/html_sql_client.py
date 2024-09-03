__author__ = 'Yossi'

import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
import webbrowser
import os

def menu():
    print(
        "1. Add Movie\n" +
        "2. What movies are shown at a certain time\n" +
        "3. Movies with the highest rating\n" +
        "4. Get All Movies\n" +
        "5. What movies are shown in the VIP screens and when\n" +
        "6. Add movie to a screen\n" +
        "7. Make screen room VIP\n" +
        "9. Exit\n\n>")

    option = input("Enter option number> ")

    if option == "9":
        return "quit"
    elif option == "1":
        movie_id = input("Enter movie ID > ")
        title = input("Enter movie title > ")
        director = input("Enter movie director > ")
        rating = input("Enter movie rating > ")
        start_time = input("Enter movie start time > ")
        return f"ADD_MOVIE|{movie_id}|{title}|{director}|{rating}|{start_time}"
    elif option == "2":
        watch_time = input("Enter the hour you want to watch a movie (e.g., 16:00) > ")
        return f"MOVIES_AT_TIME|{watch_time}"
    elif option == "3":
        limit = input("How many movie results do you wish to get? > ")
        return f"BEST_RATED_MOVIES|{limit}"
    elif option == "4":
        return "GET_ALL_MOVIES|"
    elif option == "5":
        vip_time = input("Enter the hour you want to watch a VIP movie (e.g., 16:00) > ")
        return f"VIP_MOVIES|{vip_time}"
    elif option == "6":
        screen_id = input("Enter room ID > ")
        movie_id = input("Enter movie ID > ")
        screening_time = input("Enter the time the movie is screened > ")
        return f"ADD_SCREEN|{screen_id}|{movie_id}|{screening_time}"
    elif option == "7":
        vip_screen_id = input("Enter the screen ID of the screen you want to make VIP > ")
        return f"MAKE_VIP|{vip_screen_id}"
    else:
        return "CHECK_LIVE"

def display_html(action, data):
    if action == "ADD_MOVIE":
        if data == "Success":
            message = "Movie added successfully"
        else:
            message = "Failed to add the movie"
        with open('result.html', 'w') as f:
            html_template = f"""
            <html> 
            <head></head> 
            <body> 
            <p>{message}</p> 
            </body> 
            </html> 
            """
            f.write(html_template)
        filename = f'file:///{os.getcwd()}/result.html'
        webbrowser.open_new_tab(filename)


def main():
    client_socket = socket.socket()
    client_socket.connect(("127.0.0.1", 33445))

    while True:
        user_input = menu()

        if user_input == "quit":
            break
        send_with_size(client_socket, user_input)

        response = recv_by_size(client_socket)
        if not response:
            print("Server disconnected")
            break
        response = response.decode()
        print("Received: " + response)
        action = response[:3]
        data = response[4:]

        display_html(action, data)

if __name__ == "__main__":
    main()
