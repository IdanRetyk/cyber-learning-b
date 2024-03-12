import pyautogui

SCREENSHOTS_FOLDER = rf'C:\cyber-learning-b\27screen'

def take_screenshot(save_name):
   
    try:
        img = pyautogui.screenshot()
        img.save(rf'{SCREENSHOTS_FOLDER}\{save_name}.jpg')
        return True
    except Exception as err:
        return False



take_screenshot(input("name "))