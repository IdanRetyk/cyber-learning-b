import sys

with open(sys.argv[1],'r') as file:
    lines = file.readlines()
    
# pubiku_stack = list()


letters_dict = {'x':{"stack":["Empty"] * 100,"output":0}}

x_stack = ["Empty"] * 100
a_stack = ["Empty"] * 100
sp = 0
x_output = ""
for line in lines:
    fields = line.split()
    if len(fields) == 0:
        continue
    if fields[0] == "chu":
        # push 
        x_stack.append(fields[1])
        
    if fields[0] == "pabiku":
        # pop
        if fields[1] == "!x":
            x_output = x_stack.pop()
        if fields[1] == "!a":
            a_output = a_stack.pop()
    if fields[0] == "pika":
        print(x_output)
    #     pubiku_stack.append(line.split()[-1])
    # if "pabiku !x" in line or "pabiku !a" in line:
    #     head = pubiku_stack.pop()
    # if "pika" in line:
    #     print(head)


