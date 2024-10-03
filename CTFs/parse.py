import sys

with open(sys.argv[1],'r') as file:
    lines = file.readlines()
    
# pubiku_stack = list()
stack = ["Empty"] * 100
sp = 0
pika_output = ""
for line in lines:
    fields = line.split()
    if len(fields) == 0:
        continue
    if fields[0] == "chu":
        # push 
        sp += 1
        stack[sp] = fields[1]
    if fields[0] == "pabiku":
        if fields[1] == "!x":
            pika_output = stack[sp]
            sp -= 1
        if fields[1] == "!a":
            # pika_output = stack[sp]
            sp -= 1
    if fields[0] == "pika":
        print(pika_output)
    #     pubiku_stack.append(line.split()[-1])
    # if "pabiku !x" in line or "pabiku !a" in line:
    #     head = pubiku_stack.pop()
    # if "pika" in line:
    #     print(head)


