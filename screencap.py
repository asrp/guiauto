import ctypes
import numpy
import os

lib_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c_screencap.so')
c_screencap = ctypes.CDLL(lib_filename)
c_screencap.getScreen.argtypes = []

def screencap(width, height, x=0, y=0):
    objsize = width * height * 3

    # return c_screencap.getScreen(x, y, w, h)
    result = (ctypes.c_ubyte * objsize)()
    c_screencap.getScreen(x, y, width, height, result)
    return numpy.array(result, numpy.uint8).reshape([height, width, 3])

if __name__ == '__main__':
    from PIL import Image
    im = screencap(1200, 1000)
    Image.fromarray(im).show()
