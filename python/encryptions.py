import base64,re,random,itertools
# number 1 

def encrypt1(message, key):
    return "".join([chr(ord(x) + int(key[0])) for x in message])

def decrypt1(message = "Wkh#dwwdfn#zloo#vwduw#dw#vxqvhw",key = "309"):
    return "".join([chr(ord(x) - int(key[0])) for x in message])

print(decrypt1()) #The attack will start at sunset


#number 2 
#vvvvvvvvvvvv
def encrypt2(message,key):
    return base64.b64encode("".join([chr(ord(message[i]) ^ ord(key [i % len(key)])) for i in range(len(message ))]).encode())

def decrypt2(chiper,key):
    return "".join([chr(b ^ ord(key[i % len(key)])) for i, b in enumerate( base64.b64decode(chiper))])


for i in range(10000):
    key = str(i).zfill(4)

    msg = decrypt2("YVxcGVRATVhWXxlOXFhVGUZAWEtBFFZXFWBMXEZQWEAVWVZLW11XXg==",key)
    if (re.search("^[A-Z a-z]*$",msg)):
        print(msg) # The attack will start on Tuesday morning



#number 3
#vvvvvvvvvvvvvvvv
def encrypt3(message, key): #this shuffles the string
    random.seed(key)
    l = list(range(len(message)))
    random.shuffle(l) 
    return "".join([message[x] for x in l])

def decrypt3(chiper,key):
    random.seed(key)
    l = list(range(len(chiper)))
    random.shuffle(l)
    if (chiper[l.index(0)] != 'T'):
        return ""
    return "".join([chiper[l.index(i)] for i in range(len(chiper))] )

message = "kth tntTeia0lt a lua1 dtt: ro5 Scasa0 wary"

for i in itertools.permutations("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" , 3):
    dcrptd = decrypt3(message,"".join([str(i[x]) for x in range(3)]))
    if ("The attack" in dcrptd):
        print (dcrptd)
        
        


