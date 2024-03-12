
Instractions:

Take the maze pic maze.png
the start is at top right and the end at bottom left,
the walls are black
try to find the way to exit ! please don't do that by your hands and eyes !!!!
there is only one single path from start to exit.



use :
1. from PIL import Image
2. google about Image and learn about :  open , size,  putpixel, getpixel,  save
(also see:  box, crop, paste   but you don't need it here)
3. put other color (red or green) in the solution way and save it other name
4. solution can be done in 23 lines


5. if you want...here algorithm idea: skip reading this if you want to think by your self
	1. Go from exit till start and put in dict all "valid links" between two pixels
	(but only one direction (to end) ) example:  my_dict[next_valid_point] = current_valid_point
	2. Then, build the path : go from start to exit by using these links

6. sone help put this in start and play with it :

maze = Image.open("maze.png")
links = {}
directions = (0, 1), (0, -1), (1, 0), (-1, 0)
path_color = (255,) *4
border = (0,0,0,255)
width, height = maze.size
maze.putpixel((1, height - 1), border)
maze.putpixel((width - 2, 0), border)
open_list = [(1, height - 2)]
links[open_list[0]] = '!'
