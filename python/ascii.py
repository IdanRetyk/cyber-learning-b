'''
author : Ophir Hoffman (yud alef 3)
'''

from PIL import Image
import cv2
import numpy as np


def get_ascii_char(color):

    chars = ' .;-:!>7?CO$QHNM'
    
    avg = color[0] + color[1] + color[2]
    avg = avg // 3
    
    return chars[avg//16]

    
def get_frame(pic):
    
    img = Image.fromarray(pic)
   

    width, height = img.size

    pixels = img.load()
    
    result = ""

    for r in range(0, height-1,5):
        for c in range(0, width-1,5):
            result += get_ascii_char(pixels[c,r])
        result += '\n'

    return result

    
    
def show_video():
    
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture("bar.jpg")
     
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
      print("Error opening video stream or file")
     
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
      ret, frame = cap.read()
      if ret == True:
     
        # Display the resulting frame
        frame = get_frame(frame)
            
        print(frame)
     
        # Press Q on keyboard to  exit
        cv2.waitKey(35)
     
      # Break the loop
      # if keyboard.is_pressed('q'): 
        # break
     
    # When everything done, release the video capture object
    cap.release()
     
    # Closes all the frames
    cv2.destroyAllWindows()


show_video()