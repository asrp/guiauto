from Xlib import X, XK, display
from Xlib.ext.xtest import fake_input

# 1, 2, 3
LEFT = X.Button1
MIDDLE = X.Button2
RIGHT = X.Button3

def move(x, y, duration=0):
    disp = display.Display()
    root = disp.screen().root
    root.warp_pointer(x, y)
    disp.sync()

def click(button=LEFT):
    d = display.Display()
    fake_input(d, X.ButtonPress, button)
    d.sync()
    fake_input(d, X.ButtonRelease, button)
    d.sync()

def get_position():
    qp = display.Display().screen().root.query_pointer()
    return qp.root_x, qp.root_y

def string_to_keycode(d, key):
    return d.keysym_to_keycode(XK.string_to_keysym(key))

def press(key, mod=()):
    d = display.Display()
    keycode = string_to_keycode(d, key)
    for mod_key in mod:
        fake_input(d, X.KeyPress, string_to_keycode(d, mod_key))
    fake_input(d, X.KeyPress, keycode)
    d.sync()
    fake_input(d, X.KeyRelease, keycode)
    for mod_key in mod:
        fake_input(d, X.KeyRelease, string_to_keycode(d, mod_key))
    d.sync()
