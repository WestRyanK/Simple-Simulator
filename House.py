import random
from Mailbox import *
from Object3D import *
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

def generateNeighborhood():
    neighborhood = []
    spacing = 15
    blockSize = 3
    streetSize = 30
    addBlock(neighborhood, blockSize, blockSize, spacing, 30, -10)
    addBlock(neighborhood, blockSize, blockSize, spacing, 30, 55)

    return neighborhood

def addBlock(neighborhood, blockX = 6, blockZ = 6, spacing = 15, x = 0, z = 0):
    addStreet(neighborhood, blockX - 1, 15, 0, x, z)
    addStreet(neighborhood, blockZ - 1, 15, -90, x + spacing * (blockX - 1), z)
    addStreet(neighborhood, blockX - 1, 15, -180, x + spacing * (blockX - 1), z - spacing * (blockZ - 1))
    addStreet(neighborhood, blockZ - 1, 15, 90, x, z - spacing * (blockZ - 1))

def addStreet(neighborhood, lineCount = 6, spacing = 15, angle = 0, x = 0, z = 0):
    radianAngle = math.radians(angle)
    for i in range(lineCount):
        w = random.random() * 8 + 5
        l = random.random() * 10 + 5
        h = random.random() * 2 + 4
        house = House(x + math.cos(radianAngle) * i * spacing, z + math.sin(radianAngle) * i * spacing, angle, w, h, l)
        neighborhood.append(house)


class House(Object3D):
    def __init__(self, positionX = 0, positionZ = 0, rotationY = 0, width = 10, height = 5, length = 10): 
        Object3D.__init__(self, positionX = positionX, positionZ = positionZ, rotationY = rotationY)
        self.colorR = random.random()
        self.colorG = random.random()
        self.colorB = random.random()
        self.checkCollisions = True
        self.mass = 15
        self.size = np.array([width, height, length], dtype=float)

    def collisionCallback(self, otherObject, initialVelocitySelf, initialVelocityOther):
        speed = magnitude(initialVelocitySelf - initialVelocityOther) * 0.1
        self.velocity[1] = min(0.4, speed)
        self.update()

    def drawObject(self):
        w= self.size[0] / 2.0
        h= self.size[1]
        r = h + 3
        l= self.size[2] / 2.0

        glLineWidth(2.5)
        glColor3f(self.colorR, self.colorG, self.colorB)
        # walls 
        glBegin(GL_QUADS)
        glVertex3f(-w,0,-l)
        glVertex3f(-w,h,-l)
        glVertex3f(-w,h,l)
        glVertex3f(-w,0,l)
        glVertex3f(-w,0,l)
        glVertex3f(-w,h,l)
        glVertex3f(w,h,l)
        glVertex3f(w,0,l)
        glVertex3f(w,0,l)
        glVertex3f(w,h,l)
        glVertex3f(w,h,-l)
        glVertex3f(w,0,-l)
        glVertex3f(w,h,-l)
        glVertex3f(w,0,-l)
        glVertex3f(-w,0,-l)
        glVertex3f(-w,h,-l)
        #Roof
        glColor3f(0.4, 0.3, 0.2)
        glVertex3f(-w, h, -l)
        glVertex3f(0, r, -l)
        glVertex3f(0, r, l)
        glVertex3f(-w, h, l)

        glVertex3f(w, h, -l)
        glVertex3f(0, r, -l)
        glVertex3f(0, r, l)
        glVertex3f(w, h, l)

        glColor3f(self.colorR, self.colorG, self.colorB)
        glVertex3f(0, r, l)
        glVertex3f(w, h, l)
        glVertex3f(0, h, l)
        glVertex3f(-w, h, l)

        glVertex3f(0, r, -l)
        glVertex3f(w, h, -l)
        glVertex3f(0, h, -l)
        glVertex3f(-w, h, -l)
        
        #Door
        glColor3f(0.4, 0.4, 0.4)
        glVertex3f(-1, 0, l + .1)
        glVertex3f(-1, 3, l + .1)
        glVertex3f(1, 3, l + .1)
        glVertex3f(1, 0, l + .1)
        glEnd()
        glColor3f(0, 0, 0)
        #Floor
        glBegin(GL_LINES)
        glVertex3f(-w, 0, -l)
        glVertex3f(w, 0, -l)
        glVertex3f(w, 0, -l)
        glVertex3f(w, 0, l)
        glVertex3f(w, 0, l)
        glVertex3f(-w, 0, l)
        glVertex3f(-w, 0, l)
        glVertex3f(-w, 0, -l)
        #Ceiling
        glVertex3f(-w, h, -l)
        glVertex3f(w, h, -l)
        glVertex3f(w, h, -l)
        glVertex3f(w, h, l)
        glVertex3f(w, h, l)
        glVertex3f(-w, h, l)
        glVertex3f(-w, h, l)
        glVertex3f(-w, h, -l)
        #Walls
        glVertex3f(-w, 0, -l)
        glVertex3f(-w, h, -l)
        glVertex3f(w, 0, -l)
        glVertex3f(w, h, -l)
        glVertex3f(w, 0, l)
        glVertex3f(w, h, l)
        glVertex3f(-w, 0, l)
        glVertex3f(-w, h, l)
        #Door
        glVertex3f(-1, 0, l + .1)
        glVertex3f(-1, 3, l + .1)
        glVertex3f(-1, 3, l + .1)
        glVertex3f(1, 3, l + .1)
        glVertex3f(1, 3, l + .1)
        glVertex3f(1, 0, l + .1)
        #Roof
        glVertex3f(-w, h, -l)
        glVertex3f(0, r, -l)
        glVertex3f(0, r, -l)
        glVertex3f(w, h, -l)
        glVertex3f(-w, h, l)
        glVertex3f(0, r, l)
        glVertex3f(0, r, l)
        glVertex3f(w, h, l)
        glVertex3f(0, r, l)
        glVertex3f(0, r, -l)
        glEnd()