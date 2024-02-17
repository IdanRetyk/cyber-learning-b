from PIL import Image


def load_img_as_array():
    #returns the image as a 2d array of the pixels
    
    img = Image.open("/Users/Idan/cyber-learning-b/maze/maze.png")
    img = img.convert("RGB")
    pixels = img.getdata()
    
    h,w = 639,639
    mat = [[0 for x in range(w)] for y in range(h)] 
    
    for y in range(639):
        for x in range(639):
            pixel = pixels[y * 639 + x] 
            if(pixel[0] == 0): #black
                mat[x][y] = 0
            else:
                mat[x][y] = 255

    return mat
                

all_to_die = False


def valid_pixel(x,y,visited,img): #this function will check if the recurstion needs to end

    if (x > 638 or x < 0 or y > 638 or y < 0 ):
        print(f"out of range {x},{y} ")
        return False
    
    if (visited[y][x]):
        print(f"visited {x},{y} ")
        return False
    
    if (img[y][x] == 0):
        print(f"black pixel {x},{y} ")
        return False
    
    return True


def deep_first_search(img,link,x,y,visited,direction):
    
    
    
    
    if (x == 0 and y == 638):
        draw_solution(link)
        return
    
    link.append((x,y))
    
    visited[y][x] = True
    try:
        if (direction != "down") :
            print("moved up ")
            if (valid_pixel(x,y + 1,visited,img)):
                deep_first_search(img,link,x,y + 1,visited,"up")
            
        if (direction != "up"):
            print("moved down")
            if (valid_pixel(x,y - 1,visited,img)):
                deep_first_search(img,link,x,y - 1,visited,"down")
            
        if (direction != "left"):
            print("moved right")
            if (valid_pixel(x - 1,y,visited,img)):
                deep_first_search(img,link,x - 1,y,visited,"right")
            
        if (direction != "right"):
            print("moved left")
            if (valid_pixel(x + 1,y,visited,img)):
                deep_first_search(img,link,x + 1,y,visited,"left")
    
    except:
        print("Error")

    
    
        

def draw_solution(solution = [],visited = []):
    with open("maze.txt", 'w') as file:
        file.write(str(visited))


def main():
    img_arr = load_img_as_array()
    visited = [[False for x in range(639)] for y in range(639)] 
    link = []
    deep_first_search(img_arr,link,638,0,visited,"down")




if __name__ == "__main__":
    main()