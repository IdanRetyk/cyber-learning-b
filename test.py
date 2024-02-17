import time

start = time.time()

n = 0
while (n < 1000000000):
    n +=1

end = time.time()
print(n)
print(end-start)