import random
from Object3D import *
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

def generateMailboxes():
    boxes = []
    boxes.append(Mailbox(20,20,90))
    boxes.append(Mailbox(20,35,90))
    boxes.append(Mailbox(20,50,90))
    return boxes

class Mailbox(Object3D):
    def __init__(self, positionX = 0, positionZ = 0, rotationY = 0, boxWidth = 0.2, boxLength = 0.4, boxHeight = 0.2, postHeight = 1): 
        Object3D.__init__(self, positionX = positionX, positionZ = positionZ, rotationY = rotationY)
        self.colorR = random.random()
        self.colorG = random.random()
        self.colorB = random.random()
        self.checkCollisions = True
        self.mass = 10
        self.boxWidth = boxWidth
        self.boxLength = boxLength
        self.boxHeight = boxHeight
        self.postHeight = postHeight
        self.isFallingOver = False
        self.size = np.array([boxWidth, postHeight + boxHeight * 2, boxLength], dtype=float)

    def reset(self):
        Object3D.reset(self)
        self.isFallingOver = False
        self.checkCollisions = True

    def update(self, elapsedTime):
        Object3D.update(self)
        if (self.isFallingOver and self.rotation[2] < 90):
            self.rotation[2] += self.rotation[2] * 0.1 + 1 
            if (self.rotation[2] > 90):
                self.rotation[2] = 90


    def collisionCallback(self, otherObject, initialVelocitySelf, initialVelocityOther):
        self.isFallingOver = True
        self.checkCollisions = False
        # speed = magnitude(initialVelocitySelf - initialVelocityOther) * 0.1
        # self.velocity[1] = min(0.4, speed)
        # self.update()
        
    def drawObject(self):
        glPushMatrix()
        glRotatef(self.rotation[2], 0, 0, 1)
        glLineWidth(4)
        glColor3f(0,0,0)
        glBegin(GL_LINES)
        glVertex(0,0,0)
        glVertex(0,self.postHeight,0)
        glEnd()
        self.drawBox()
        glPopMatrix()

    def drawBox(self):
        glPushMatrix()
        glTranslatef(0,self.postHeight, 0)
        glColor3f(self.colorR, self.colorG, self.colorB)
        glBegin(GL_QUADS)
        # bottom
        glVertex(self.boxWidth, 0, self.boxLength)
        glVertex(-self.boxWidth, 0, self.boxLength)
        glVertex(-self.boxWidth, 0, -self.boxLength)
        glVertex(self.boxWidth, 0, -self.boxLength)

        # top
        glVertex(self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, -self.boxLength)

        # front
        glVertex(self.boxWidth, 0, self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, 0, self.boxLength)

        # back
        glVertex(self.boxWidth, 0, -self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(-self.boxWidth, 0, -self.boxLength)

        # right
        glVertex(self.boxWidth, 0, self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(self.boxWidth, 0, -self.boxLength)

        # left
        glVertex(-self.boxWidth, 0, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(-self.boxWidth, 0, -self.boxLength)
        glEnd()

        glLineWidth(2.4)
        glColor3f(0,0,0)
        glBegin(GL_LINES)
        # top
        glVertex(self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, self.boxLength)

        # front
        glVertex(self.boxWidth, 0, self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, self.boxLength)
        glVertex(-self.boxWidth, 0, self.boxLength)
        glVertex(-self.boxWidth, 0, self.boxLength)
        glVertex(self.boxWidth, 0, self.boxLength)

        # back
        glVertex(self.boxWidth, 0, -self.boxLength)
        glVertex(self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(-self.boxWidth, self.boxHeight * 2, -self.boxLength)
        glVertex(-self.boxWidth, 0, -self.boxLength)
        glVertex(-self.boxWidth, 0, -self.boxLength)
        glVertex(self.boxWidth, 0, -self.boxLength)

        # right
        glVertex(self.boxWidth, 0, self.boxLength)
        glVertex(self.boxWidth, 0, -self.boxLength)

        # left
        glVertex(-self.boxWidth, 0, self.boxLength)
        glVertex(-self.boxWidth, 0, -self.boxLength)
        glEnd()
        glPopMatrix()
