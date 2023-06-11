import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import re
import pyautogui
import cv2
import numpy as np
import os
import time


os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Save screenshots every second to __img__ folder

x = 0

while True:
    img = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # save nth screenshot

    # save nth screenshot
    cv2.imwrite("./img/screenshot{}.png".format(x), img)
    x += 1
    # wait 1 second
    time.sleep(1)



def find_window_by_title(title_pattern):
    desired_windows = []

    def enum_windows_callback(hwnd, extra):
        window_title = win32gui.GetWindowText(hwnd)
        if re.match(title_pattern, window_title):
            # print location and size
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            print("Window %s:" % win32gui.GetWindowText(hwnd))
            print("\tLocation: (%d, %d)" % (x, y))
            print("\t    Size: (%d, %d)" % (w, h))

            extra.append(hwnd)

    win32gui.EnumWindows(enum_windows_callback, desired_windows)

    return desired_windows

hwnd = find_window_by_title('War')[0]

# Change the line below depending on whether you want the whole window
# or just the client area. 
#left, top, right, bot = win32gui.GetClientRect(hwnd)
left, top, right, bot = win32gui.GetWindowRect(hwnd)
w = right - left
h = bot - top

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

# Change the line below depending on whether you want the whole window
# or just the client area. 
#result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
print(result)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

if result == 1:
    #PrintWindow Succeeded
    im.save("test.png")
