
*setup*
run following commands on any device you wish to run either server or client.
pip install pygame
pip install treys

if you get any errors, make you sure you have pip installed and in the path.


In game_server.py, change PLAYER_COUNT to the desired amount of players (2-5), than run it.

In client.py, change the IP variable to the ip of the device on which the server runs. To check the ip, type ipconfig and find the default gateway.
Every player need to run client.py .


*brief explanation of the game*

Every player sees the poker board. Every player chooses their name and money amount, and they can see it in the bottom. every other player's stats are visible as well.

The game works in turns. If it's your turn, you will see in the screen button appear, and you need to choose what is your move between three options. Betting, checking or folding. In some cases,
you may not have all of these, or instead have raising/calling. If you fold, you will be out of the hand without a chance to gain back you money. checking is the equivalent of skipping you turn, and betting is putting money in. When all the players either have folded or betted the same amount, the next card is revealed. When all cards are revealed, or all but one fold the winner is announced and the next hand will now take place.

The game also includes more complex concepts such as blinds, and bet jumps. For a more thorough explanation check out this article. 



*networking details*

The game_server.py file runs the server, and is responsible for transferring the moves the players make to every other player. The game_server.py itself is not a player.

The network communication is done using python builtin socket module. In this project the communication is above UDP.

The server opens a udp socket, and every client opens their own socket, and the communication is between the server socket and the client socket.

Every message is sent in a loop, until receiving ACK message. This is implemented using the recv_ack, and send_data_ack functions in the function.py module.

Because UDP has no concept of connections, when we receive data, we make sure it is the right message, in case several client sent message at the same time, and while expecting
a message from client A with a specific format, we received a message from client B, in a different format.

The game implements a waiting room. The server waits until there are the specified amount of players before starting the game. This is implemented in the waiting_room function in 
game_server.py, and in client_hello in client.py. This part has no GUI yet, so it just prints a message. The case of clients disconnecting during the waiting room is not handled.

During the game itself, the player who's turn is to play, receives a TURN message. Than after the player chooses its move, client sends back to server MOVE message. Server will broadcast to all players, and they will update their GUI. This is the main game loop. In game_server.py this is in the handle_game function, in the client its in GUI.__init__()

The game will continue until a client exits, brutally or not. Even if one client exits brutally, the server realizes that, and sends an exit message to the other players, and they exit as well.



*other programming details*

The server holds a game object, and so does every player. When the server receives the move from the player, it updates its own game object and than broadcast the move, and every player updates its own game object when receiving the move message.
The client holds a game object, and a player object.

folder explanation - 
 - pictures: contains all the photos.
 - classes.py: contains all the classes used.
 - functions.py: contains all the functions useful both for server and client. mainly networking related.
 - game.server.py: game server.
 - client.py: player.

classes explanation - 
 - Card: represent a card. Has a suit and a value.
 - CardDeck: a deck of cards. A list of cards, of which you can draw, and shuffle.
 - Player: A player. Contains all the important data about a player both game related and networking related.
 - Game: A game. This is the only object that is actually being used, and this one uses all the others. Contains mainly a list of players, and a list of cards. 


The money and names of other players are shown in order, with the playing player in the middle position. This is done in update_gui in the client. It rotates the location list such that the player position index moves to the 0th index. 