from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

keyHandler = None

class KeyHandler:
    def __init__(self):
        self.keyState = {
            b'q' : False,
            b'w' : False,
            b'e' : False,
            b'r' : False,
            b't' : False,
            b'y' : False,
            b'u' : False,
            b'i' : False,
            b'o' : False,
            b'p' : False,
            b'a' : False,
            b's' : False,
            b'd' : False,
            b'f' : False,
            b'g' : False,
            b'h' : False,
            b'j' : False,
            b'k' : False,
            b'l' : False,
            b'z' : False,
            b'x' : False,
            b'c' : False,
            b'v' : False,
            b'b' : False,
            b'n' : False,
            b'm' : False,
            chr(27) : False}
        glutKeyboardFunc(buildKeyboardStateDown)
        glutKeyboardUpFunc(buildKeyboardStateUp)
        global keyHandler
        keyHandler = self


    def buildKeyboardState(self, key, isDown):
        if (key == b'q'): 
            self.keyState[b'q'] = isDown
        if (key == b'w'): 
            self.keyState[b'w'] = isDown
        if (key == b'e'): 
            self.keyState[b'e'] = isDown
        if (key == b'r'): 
            self.keyState[b'r'] = isDown
        if (key == b't'): 
            self.keyState[b't'] = isDown
        if (key == b'y'): 
            self.keyState[b'y'] = isDown
        if (key == b'u'): 
            self.keyState[b'u'] = isDown
        if (key == b'i'): 
            self.keyState[b'i'] = isDown
        if (key == b'o'): 
            self.keyState[b'o'] = isDown
        if (key == b'p'): 
            self.keyState[b'p'] = isDown
        if (key == b'a'): 
            self.keyState[b'a'] = isDown
        if (key == b's'): 
            self.keyState[b's'] = isDown
        if (key == b'd'): 
            self.keyState[b'd'] = isDown
        if (key == b'f'): 
            self.keyState[b'f'] = isDown
        if (key == b'g'): 
            self.keyState[b'g'] = isDown
        if (key == b'h'): 
            self.keyState[b'h'] = isDown
        if (key == b'j'): 
            self.keyState[b'j'] = isDown
        if (key == b'k'): 
            self.keyState[b'k'] = isDown
        if (key == b'l'): 
            self.keyState[b'l'] = isDown
        if (key == b'z'): 
            self.keyState[b'z'] = isDown
        if (key == b'x'): 
            self.keyState[b'x'] = isDown
        if (key == b'c'): 
            self.keyState[b'c'] = isDown
        if (key == b'v'): 
            self.keyState[b'v'] = isDown
        if (key == b'b'): 
            self.keyState[b'b'] = isDown
        if (key == b'n'): 
            self.keyState[b'n'] = isDown
        if (key == b'm'): 
            self.keyState[b'm'] = isDown
        if (key == chr(27)):
            self.keyState[chr(27)] = isDown

def buildKeyboardStateDown(key, x, y):
    global keyHandler
    keyHandler.buildKeyboardState(key, True)

def buildKeyboardStateUp(key, x, y):
    global keyHandler
    keyHandler.buildKeyboardState(key, False)
