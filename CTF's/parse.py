import sys

with open(sys.argv[1],'r') as file:
    lines = file.readlines()
    
# pubiku_stack = list()
stack = [None] * 100
sp = 0
for line in lines:
    if "chu" in line:
        # push 
        sp += 1
    #     pubiku_stack.append(line.split()[-1])
    # if "pabiku !x" in line or "pabiku !a" in line:
    #     head = pubiku_stack.pop()
    # if "pika" in line:
    #     print(head)