from PIL import Image


def load_img_as_array(image_path = "/Users/Idan/cyber-learning-b/maze/maze2.png"):
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    img_arr = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel_value = pixels[x, y]
            row.append(pixel_value)
        img_arr.append(row)
    return img_arr


img_arr = load_img_as_array()
for _ in img_arr:
    print(_)
    print()
img = Image.new("RGB", (641, 641))
pixels = img.load()
for y in range(len(img_arr)):
    for x in range(len(img_arr[0])):
        if(img_arr[y][x] == 0):
            pixels[x, y] = 0
        else:
            pixels[x, y] = (255,255,255) 
img.save("start.png")