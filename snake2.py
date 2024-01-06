#snake 2



def main():
    with open("encrypted.jpg", "rb") as image:
        byteArr = bytearray(image.read()) 
        cnt = 0
        decBytes=[]
        for byte in byteArr :
            #print(type(byt))
            byte=((byte//16) + 16 * (byte % 16))#rotate left 4 times
            if cnt == 0 :# i it is 
                cnt = -3
                byte ^=255
            byte ^= 186
            byte = byte & 255
            decBytes.append(byte)
            cnt += 1
        img_bytes = bytes(bytearray(decBytes[::-1]))
        with open("decrypted.jpg", "wb") as write_to:
            print("done")
            write_to.write(img_bytes)
            
            
if __name__ == "__main__":
    main()


