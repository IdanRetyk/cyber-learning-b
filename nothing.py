import time

start = time.time()

n = 100000000
for i in range(n):
    i += 1

end = time.time()
print(f"time = {end - start}, {i}")