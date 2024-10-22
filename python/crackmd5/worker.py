import sys

from hashlib import md5


if len((sys.argv))!= 3:
    print("Wrong usage")
    exit()

start = int(sys.argv[1])
end = int(sys.argv[2])
TARGET = sys.argv[3].encode()


for i in range(start,end):
    if md5(bytes(i)).digest() == TARGET:
            print(f"FOUND~{i}")
            exit()
print("NO")

