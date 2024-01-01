import socket

#global



def clinet(port):
    cont = True
    c = socket.socket()
    c.connect(("127.0.0.1",port))
    print("connected to port " + str(port))
    st = input("")
    if (st == "exit"):
        cont = False
    print("A sent " + st)
    c.send(st.encode())
    print("disconnecting")
    c.close()
    return cont
    
def server(port):
    cont = True
    server = socket.socket()
    server.bind(("127.0.0.1",port))
    print("A listeing in port " + str(port))
    server.listen(100)
    c,a = server.accept()
    data = c.recv(1024)
    if (data == "exit".encode() or data == b''):
        cont = False
    print("A recived " + data.decode())
    c.close()
    server.close()
    return cont


    
def main():
    port = 8000
    cont = True
    while (cont):
        cont = clinet(port)
        if (not cont):
            break
        port -= hash(port) % 101 * 10
        cont = server(port)
        
        for i in range(100): #its very unlikly the port will stay the same after this
            port += hash(port) % (i + 1)

if __name__ == "__main__":
    main()