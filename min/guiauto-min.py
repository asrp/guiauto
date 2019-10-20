from Xlib import display, X
from Xlib.ext.xtest import fake_input
from PIL import Image
import cv2
import numpy

def find_best(needle, haystack):
    match = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    return max_loc, max_val

def screencap(x, y, w, h):
    root = display.Display().screen().root
    raw = root.get_image(x, y, w, h, X.ZPixmap, 0xffffffff)
    return Image.frombytes("RGB", (w, h), raw.data, "raw", "BGRX")

def mouse_move(x, y):
    disp = display.Display()
    root = disp.screen().root
    root.warp_pointer(x, y)
    disp.sync()

def mouse_click(button=1):
    disp = display.Display()
    fake_input(disp, X.ButtonPress, button)
    disp.sync()
    fake_input(disp, X.ButtonRelease, button)
    disp.sync()

def find_on_screen(image):
    needle = cv2.imread(image)
    screen = display.Display().screen()
    width, height = screen.width_in_pixels, screen.height_in_pixels
    haystack = numpy.array(screencap(0, 0, width, height))
    return needle.shape[1::-1], find_best(needle, haystack)

def click(image, similarity=0.7):
    shape, (pos, confidence) = find_on_screen(image)
    if confidence > similarity:
        center = [int(p + s/2) for p, s in zip(pos, shape)]
        mouse_move(*center)
        mouse_click()

if __name__ == '__main__':
    click("image.png")
