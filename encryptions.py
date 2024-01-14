import base64,re
# number 1 

def encrypt1(message, key):
    return "".join([chr(ord(x) + int(key[0])) for x in message])

def decrypt1(message = "Wkh#dwwdfn#zloo#vwduw#dw#vxqvhw",key = "309"):
    return "".join([chr(ord(x) - int(key[0])) for x in message])

print(decrypt1()) #The attack will start at sunset


#number 2 

def encrypt2(message,key):
    return base64.b64encode("".join([chr(ord(message[i]) ^ ord(key [i % len(key)])) for i in range(len(message ))]).encode())

def decrypt2(message,key):
    return "".join([chr(b ^ ord(key[i % len(key)])) for i, b in enumerate( base64.b64decode(message))])

for i in range(10000):
    key = str(i).zfill(4)

    msg = decrypt2("YVxcGVRATVhWXxlOXFhVGUZAWEtBFFZXFWBMXEZQWEAVWVZLW11XXg==",key)
    if (re.search("^[A-Z a-z]*$",msg)):
        print(msg)