import socket


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(("0.0.0.0",1234))

print("Waiting for message")
print(s.recvfrom(1024))
print("Program ended")