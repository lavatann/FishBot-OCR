from ahk import AHK
import cv2 as cv
from PIL import Image
import numpy as np
from time import time
import pyautogui
import pygetwindow
import win32gui,win32ui,win32con

titles=pygetwindow.getAllTitles()
print(titles)
ahk = AHK(executable_path='D:\\Image\\Programy\\Automatyzacja_clickery\\AutoHotkey_1.1.33.02\\AutoHotkeyU64.exe')

def load_digits():
    digits = []
    for i in range(1,6,1):
        digits.append(cv.imread('D:\\koparka\\fisher\\digits\\org\\'+str(i)+'.jpg', cv.IMREAD_UNCHANGED))
    return digits
def window_capture():

    w = 800 # set this
    h = 600 # set this

    #hwnd=None
    #hwnd = win32gui.FindWindow(None, 'Input Application')
    hwnd = win32gui.FindWindow(None, 'Vidgar')
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape=(h,w,4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = img[...,:3]
    img = np.ascontiguousarray(img)
    return img

def click_button(clicks):

    for _ in range(clicks):
        ahk.key_press('Space')
        pyautogui.sleep(0.021 )
    pyautogui.sleep(5)    
    ahk.key_press('1')    
    ahk.key_press('Space') 
    

        


loop_time = time()
x=load_digits()



while True:
    screenshot = window_capture()
    img = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(img, 120, 255, cv.THRESH_BINARY)[1]
 
    for i in range(5):
        temp_digit=x[i]
        result = cv.matchTemplate(screenshot, temp_digit, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        print('Liczba:',i,'Pewnosc: %s' % max_val)

        threshold = 0.8
        # Get the size of the needle image. With OpenCV images, you can get the dimensions 
        # via the shape property. It returns a tuple of the number of rows, columns, and 
        # channels (if the image is color):
        needle_w = temp_digit.shape[1]
        needle_h = temp_digit.shape[0]

        # Calculate the bottom right corner of the rectangle to draw
        top_left = max_loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)


        if max_val >= threshold:
            cv.rectangle(screenshot, top_left, bottom_right, 
                        color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
            #print('Found needle.')
            #print("Liczba to: ", i+1)
            clicks=i+1
            click_button(clicks)
            
        
    cv.imshow('Computer Vision', screenshot)

    










    #print('FPS: {}'.format(1/(time()-loop_time)))
    loop_time = time()
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break