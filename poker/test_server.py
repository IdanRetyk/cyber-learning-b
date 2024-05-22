from functions import send_data_ack,recv_ack
import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
send_data_ack(sock,b"MOVE",("127.0.0.1",12345),"HELLO")
d,a = recv_ack(sock,"HELLO")
print("done")