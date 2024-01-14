
import os
import socket
import threading

path = 'C:\\cyber-learning-b\\webroot'


def rec_amount(sock, size):
    d = b''
    while len(d) < size:
        data = sock.recv(size - len(d))
        if len(data) == 0:
            return b''
        d += data
    return d


def http_recv(cli_sock):
    d = b''
    # get the header
    i = 0
    while True:
        d += cli_sock.recv(8 * 1024)
        header_body = d.split(b'\r\n\r\n')
        if header_body[0] != d:
            break
    len_of_body_recv = len(header_body[1])
    header = header_body[0]
    parts = header.split(b'\r\n')
    length_of_body = 0
    for i in parts:
        if b'Content-Length' in i:
            length_of_body = int(i.split(b' ')[1].decode())
    length_of_body = length_of_body - len_of_body_recv
    d += rec_amount(cli_sock, length_of_body)

    return d


def check_get_post(d):
    header = d.split(b'\r\n\r\n')[0]
    command_line = header.split(b'\r\n')[0]
    command = command_line.split(b' ')[0]
    if command == b'GET' or command == b'POST':
        return command
    return b''


def get_next(command):
    command = command.split(b'?')[1][4::].decode()
    if command.isnumeric():
        return str(int(command) + 1).encode()
    return b''


def area_of_triangle(command):
    num1 = command.split(b'?')[1].split(b'&')[0][7::].decode()
    num2 = command.split(b'?')[1].split(b'&')[1][6::].decode()
    if num2.isnumeric() and num1.isnumeric():
        num1 = int(num1)
        num2 = int(num2)
        return str(0.5 * num1 * num2).encode()
    return b''


def get_image(command):
    path = command.split(b'=')[1]
    data = b''
    if os.path.exists('c:\\picture\\' + path.decode()):
        with open('c:\\picture\\' + path.decode(), 'rb') as file:
            data = file.read()
        return data
    return b''


def get_data_post(d):
    d = d.split(b'\r\n\r\n')
    body = d[1]
    header = d[0]
    prop = header.split(b'\r\n')[1::]
    command = header.split(b'\r\n')[0].split(b' ')[1]

    if b'/upload?file-name=' in command and command.split(b'=')[1] != b'':
        if not os.path.isdir("C:/picture"):
            os.makedirs("C:/picture")

        with open('C:\\picture\\' + command.split(b'=')[1].decode(), 'wb') as file:
            file.write(body)
        return b'', command, True
    return b'', command, False


def get_data_get(d):
    global path
    header = d.split(b'\r\n\r\n')
    header = header[0]
    command_line = header.split(b'\r\n')[0].split(b' ')
    url = command_line[1]
    command = url.replace(b'/', b'\\')

    if command == b'\\':
        with open(path + '\\index.html', 'rb') as file:
            string = file.read()
        return string, command

    elif b'\\temp.html' in command:
        return b'', command

    elif b'\\calculate-area?height=' in command and b'&width=' in command:
        return area_of_triangle(command), command

    elif b'\\calculate-next?num=' in command and command != b'\\calculate-next?num=':
        return get_num_plus_one(command), command

    elif b'\\image?image-name=' in command and command.split(b'=')[1] != b'':
        return get_image(command), command

    elif os.path.exists(path + command.decode()):
        with open(path + command.decode(), 'rb') as file:
            string = file.read()
        return string, command

    return b'', command


def protocol_build_reply(body, status, command):
    reply = b''
    reply += b'HTTP/1.0 '

    if status == 200:
        reply += b'200 '
        reply += b'OK\r\n'
    elif status == 404:
        reply += b'404 '
        reply += b'EROR\r\n'

    elif status == 403:
        reply += b'403 '
        reply += b'Forbidden\r\n'

    reply += b'Content-Length: ' + str(len(body)).encode()

    if b'calculate-area' in command:
        reply += b'\r\n'
        reply += b'Content-Type: text/plain'

    if b'calculate-next' in command:
        reply += b'\r\n'
        reply += b'Content-Type: text/plain'

    if b'jpg' in command:
        reply += b'\r\n'
        reply += b'Content-Type: image/jpeg'

    if b'js' in command:
        reply += b'\r\n'
        reply += b'Content-Type: text/javascript; charset=UTF-8'

    if b'css' in command:
        reply += b'\r\n'
        reply += b'Content-Type: text/css'
    reply += b'\r\n\r\n' + body
    return reply


def handle_client(sock, tid, addr):
    d = http_recv(sock)
    type_of_message = check_get_post(d)
    if type_of_message != b'POST' and type_of_message != b'GET':
        print('Oh no! the message you got was not a Get or POST, bye bye')
    else:
        if type_of_message == b'POST':
            data, command, ok = get_data_post(d)
            if ok:
                sock.send(protocol_build_reply(data, 200, command))
            else:
                sock.send(protocol_build_reply(data, 404, command))
        else:
            data, command = get_data_get(d)
            if data != b'':
                sock.send(protocol_build_reply(data, 200, command))
            else:
                if command == b'\\temp.html':
                    sock.send(protocol_build_reply(data, 403, command))
                else:
                    sock.send(protocol_build_reply(data, 404, command))
    sock.close()
    print(f'client number {tid} disconnected')


def main():
    print('starting')
    threads = []
    sock = socket.socket()
    sock.bind(('0.0.0.0', 80))
    sock.listen(50)
    i = 1
    while True:
        c, a = sock.accept()
        print(f"new client!!! number {i} from {a}")
        t = threading.Thread(target=handle_client, args=(c, str(i), a))
        t.start()
        i += 1


        threads.append(t)
    sock.close()


if __name__ == '__main__':
    main()