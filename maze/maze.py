from PIL import Image


def load_img_as_array():
    #returns the image as a 2d array of the pixels
    
    img = Image.open(r"C:\cyber-learning-b\maze\maze.png")
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


def deep_first_search(img,link,h,w,visited,direction):
    if (h > 638 or h < 0 or w > 638 or w < 0 ):
        return
    
    if (img[h][w] == 0):
        
        return
    
    if (visited[h][w]):
        return
    
    if (h == 0 and w==638):
        draw_solution(link)
        return
    
    link.append((h,w))
    visited[h][w]=True
    print(visited[h][w])
    if (direction != "down") :
        deep_first_search(img,link,h - 1,w,visited,"up")
    if (direction != "up"):
        deep_first_search(img,link,h - 1,w,visited,"down")
    if (direction != "left"):
        deep_first_search(img,link,h,w-1,visited,"right")
    if (direction != "right"):
        deep_first_search(img,link,h,w+1,visited,"left")
    
    
        

def draw_solution(solution):
    print("solutoes")
    print(solution)


def main():
    img_arr = load_img_as_array()
    visited = [[False for x in range(639)] for y in range(639)] 
    link = []
    deep_first_search(img_arr,link,638,0,visited,"down")
    print("this is"  + str(visited[638][0]))




if __name__ == "__main__":
    main()