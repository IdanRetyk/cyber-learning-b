from PIL import Image
from collections import deque
import time,random


PATH = r"/Users/Idan/cyber-learning-b/maze"
COLOR = tuple([random.randint(0,255) for _ in range(3)]) #random color

class Point:
    def __init__(self,x,y) :
        self.x = x
        self.y = y
        
    def GetDown(self):
        return Point(self.x,self.y + 1)
    def GetUp(self):
        return Point(self.x,self.y - 1)
    def GetLeft(self):
        return Point(self.x - 1,self.y)
    def GetRight(self):
        return Point(self.x + 1, self.y)
    
    @staticmethod
    def GetDirection(prev,curr):
        if (prev.x == curr.x):
            if (prev.y + 1 == curr.y):
                return "Down"
            else:
                return "Up"
        else:
            if (prev.x + 1 == curr.x):
                return "Right"
            else:
                return "Left"
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        return hash(self.x + self.y)

    def __repr__(self):
        return f"{self.x},{self.y}"
    
    
    
    def IsValid(self):
        global img_arr,visited
        if self.x > 640 or self.x < 0 or self.y > 640 or self.y < 0:
            return False

        if visited[self.x][self.y] or img_arr[self.y][self.x][0] < 10:
            return False

        return True



# end of class

def load_img_as_array(image_path = PATH):
    img = Image.open(rf"{image_path}/maze.png").convert("RGB")
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



def deep_first_search(link,stack):
    # Performs a depth-first search
    cont = True
    while(cont):
        prev,curr = stack.pop()
        if curr.IsValid():
            if curr.x == 1 and curr.y == 640:
                cont = False
                draw_solution(link)
                break
            
            link[prev] = curr
            direction = Point.GetDirection(prev,curr)
            if (direction != "Left"):
                stack.append((curr, curr.GetRight()))
            if (direction != "Down"):
                stack.append((curr, curr.GetUp()))
            if (direction != "Right"):
                stack.append((curr, curr.GetLeft()))
            if (direction != "Up"):
                stack.append((curr, curr.GetDown()))
            
            
        
        

    

def draw_solution(link):
    # Draws the solution path
    img = Image.new("RGB", (641, 641))
    pixels = img.load()

    #replicates the original maze            
    for i in range( img.size[0]):
        for j in range(img.size[1]):
            if(img_arr[j][i][0] == 0):
                pixels[i, j] = 0
            else:
                pixels[i, j] = (255,255,255)  
    
    key = Point(639,0)

    #draws path 
    while (key in link.keys()):
        
        value = link[key]
        pixels[key.x,key.y] = COLOR
        key = value

    img.save(rf"{PATH}/solved.png")


def main():
    global img_arr, visited
    
    img_arr = load_img_as_array()
    
    
    visited = [[False for _ in range(641)] for _ in range(641)]
    link = {Point(-1,-1):Point(639,0)}
    
    stack = deque()
    
    start_point = Point(639,0)
    
    stack.append((start_point,start_point.GetDown()))
    
    visited[639][0] = True

    start = time.time()
    deep_first_search(link,stack)
    end = time.time()
    st = ""
    print(f"{st:-^30}")
    print(f"finished in {end - start:.4} seconds")
    print(f"{st:-^30}")
    

    

if __name__ == "__main__":
    main()