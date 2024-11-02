import socket

s = socket.socket()

s.connect(("pwnable.kr", 9007))

s.recv(2048).decode()

def algorithm(N: int, C: int):
    start,end = 0, N
    st = b"-".join([b" ".join([str(n).encode() for n in range(start, end) if n & (1 << bit_pos)]) for bit_pos in range(C)]) + b'\n'

    print("Sets = ", len(st.split(b'-')))
    s.send(st)
    print(f"send>>>{st}")
    from_server = s.recv(2048).decode()[:-1]
    print(from_server)
    answer = 0
    for i,result in enumerate(from_server.split('-')):
        result = int(result)
        if result % 10 == 9:
            answer += result * 2 ^ i
    
    s.send(str(answer).encode() + b'\n')
    print(s.recv(1024))


def numbers_with_bit_set(start, end, bit_position):

    result = []
    mask = 1 << bit_position
    
    for number in range(start, end + 1):
        # Check if the bit at bit_position is set
        if number & mask:
            result.append(number)
    
    return result

def main():
    while True:
        from_server = s.recv(128).decode()[:-1]
        print(from_server)
        _,n,c = from_server.split("=")
        n,_ = n.split()
        algorithm(int(n),int(c))

main()

