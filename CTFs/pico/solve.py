import sys
ciphertext = input()

lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"


plain_text = ""
chars = ""
prev = 0
for char in ciphertext:
    cur = lookup2.index(char)
    original_index = (cur + prev) % 40
    chars += lookup1[original_index]
    prev = original_index
print(chars)