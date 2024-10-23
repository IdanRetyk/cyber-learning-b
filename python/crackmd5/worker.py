import sys
from hashlib import md5


if len((sys.argv))!= 4:
    print("Wrong usage")
    exit()

start = int(sys.argv[1])
end = int(sys.argv[2])
TARGET: str = sys.argv[3]




for i in range(start,end):
    if md5(str(i).zfill(10).encode()).hexdigest() == TARGET:
            print(f"FOUND~{i}")
            exit()
print("NO")

