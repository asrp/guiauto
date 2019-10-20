import cv2
import Xlib
from Xlib import display, X, protocol
import numpy
import xinput
import time
from screencap import screencap

# Todo implement rectangle bounded search
class Rect:
    def __init__(self, xy, wh):
        self.xy = numpy.array(xy)
        self.wh = numpy.array(wh)

    def center(self):
        return numpy.array([int(p + s/2) for p, s in zip(self.xy, self.wh)])

# method = cv2.TM_SQDIFF_NORMED
method = cv2.TM_CCOEFF_NORMED

def find_best(needle, haystack):
    match = cv2.matchTemplate(haystack, needle, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    if method == cv2.TM_SQDIFF_NORMED:
        return min_loc, 1 - min_val
    else:
        return max_loc, max_val

def find_on_screen(image):
    needle = cv2.imread(image)
    screen = display.Display().screen()
    haystack = screencap(screen.width_in_pixels, screen.height_in_pixels)
    return needle.shape[1::-1], find_best(needle, haystack)

def find(image, wait=0, similarity=0.7):
    start = time.time()
    while True:
        shape, (pos, confidence) = find_on_screen(image)
        # print(f'Confidence: {confidence} Image: {image}')
        if confidence > similarity:
            return Rect(pos, shape)
        elif time.time() - start > wait:
            return

def click(image, offset=(0, 0), wait=3.0):
    xy = find(image, wait=wait)
    if xy:
        xinput.move(*(xy.center() + offset))
        xinput.click()
    else:
        raise Exception("Image not found")

char_to_key = {" ": "space", ".": "period"}

def type_(s):
    for key in s:
        xinput.press(char_to_key.get(key, key))
