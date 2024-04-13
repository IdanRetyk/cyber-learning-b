from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def AES_encrypt(key:bytes, data: bytes):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return iv, ciphertext

def AES_decrypt(key : bytes, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data), AES.block_size)

