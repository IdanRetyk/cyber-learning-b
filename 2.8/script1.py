import socket

#global
cont = True


def clinet(port):
    c = socket.socket()
    c.connect(("127.0.0.1",port))
    print("connected to port " + port)
    st = input("")
    if (st == "exit"):
        cont = False
    print("A sent " + st)
    c.send(st)
    print("disconnecting")
    c.close()
    
def server(port):
    server = socket.socket()
    server.bind(("127.0.0.1",port))
    print("A listeing in port " + port)
    c,a = server.accept()
    data = c.recv(1024)
    if (data == "exit".encode()):
        cont = False
    print("A recived " + data)
        
    
def main():
    port = 8000
    while (cont):
        server(port)
        if (cont):
            clinet(port)
        
        port += hash(port) % 100

if __name__ == "__main__":
    main()