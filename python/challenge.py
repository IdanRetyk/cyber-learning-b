#python challenge - currently level 14 "italy"

from PIL import Image

img = Image.open("python/wire.png", 'r')

bytes_arr = img.load()

print(bytes_arr[0,0])
