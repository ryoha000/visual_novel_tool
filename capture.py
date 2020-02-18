import datetime
# import ctypes
# from ctypes import sizeof
from ctypes.wintypes import RECT
import win32gui
from PIL import ImageGrab
import keyboard
import mouse


print('撮りたいウィンドウをクリック')
handle = None
text = ''


def mouse_callback():
    global handle
    global text
    handle = win32gui.GetForegroundWindow()
    text = win32gui.GetWindowText(handle)


mouse.on_click(mouse_callback)

while not text:
    mouse.wait(button='left', target_types=('up',))
print('このウィンドウを撮る: ' + text)
print('違うなら再起動')

process_list = []


def callback(handle, _):
    process_list.append(win32gui.GetWindowText(handle))


win32gui.EnumWindows(callback, None)

# ターゲットウィンドウ名を探す
for process_name in process_list:
    if text in process_name:
        hnd = win32gui.FindWindow(None, process_name)
        break
else:
    # 見つからなかったら画面全体を取得
    hnd = win32gui.GetDesktopWindow()

# ウィンドウサイズ取得
x0, y0, x1, y1 = win32gui.GetWindowRect(hnd)
width = x1 - x0
height = y1 - y0

rect = RECT()
# DwmGetWindowAttribute = ctypes.windll.dwmapi.DwmGetWindowAttribute
# DWMWA_EXTENDED_FRAME_BOUNDS = 9
# DwmGetWindowAttribute(handle, DWMWA_EXTENDED_FRAME_BOUNDS,
#                       rect, sizeof(rect))
# rect = (rect.left, rect.top, rect.right, rect.bottom)
# print(rect)
rect = (x0, y0, x1, y1)
print(rect)


def key_callback():
    grabed_image = ImageGrab.grab()
    croped_image = grabed_image.crop(rect)
    name = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    filename = name + '.png'
    croped_image.save(filename)


keyboard.add_hotkey('print screen', key_callback,
                    suppress=False)

print('escキーで終了')
keyboard.wait('esc')
