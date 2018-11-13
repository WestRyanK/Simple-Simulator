import math
import numpy as np
from Util3D import *
try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import glPushMatrix
    from OpenGL.GL import glPopMatrix
except:
    print("ERROR: PyOpenGL not installed properly. ")

class Object3D:
    def __init__(self, positionX = 0, positionY = 0, positionZ = 0, rotationX = 0, rotationY = 0, rotationZ = 0, velocityX = 0, velocityY = 0, velocityZ = 0, frictionX = 0.001, frictionZ = 0.001):
        self.homePosition = np.array([positionX, positionY, positionZ], dtype=float)
        self.homeRotation = np.array([rotationX, rotationY, rotationZ], dtype=float)
        self.homeVelocity = np.array([velocityX, velocityY, velocityZ], dtype=float)
        self.checkCollisions = False
        self.size = np.array([2.0, 2.0, 2.0], dtype=float)
        self.look = np.array([0.0, 0.0, 0.0], dtype=float)
        self.homeFriction = np.array([frictionX, 0, frictionZ], dtype=float)
        self.mass = 0
        self.drawAxes = False
        Object3D.reset(self)

    def beginDraw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation[1], 0, -1, 0)

    def endDraw(self):
        glPopMatrix()

    def drawObject(self):
        glLineWidth(2.5)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0,0,0)
        glVertex3f(1,0,0)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0,0,0)
        glVertex3f(0,1,0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0,0,0)
        glVertex3f(0,0,1)
        glEnd()

    def draw(self):
        # glColor3f(0.0, 1.0, 1.0)
        # glBegin(GL_LINES)
        # glVertex3f(0,0,0)
        # glVertex3f(self.position[0], self.position[1], self.position[2])
        # glVertex3f(self.position[0], self.position[1], self.position[2])
        # glVertex3f(self.look[0], self.look[1], self.look[2])
        # glEnd()
        self.beginDraw()
        self.drawObject()
        if self.drawAxes:
            Object3D.drawObject(self)
        self.endDraw()

    def reset(self):
        self.position = np.copy(self.homePosition)
        self.rotation = np.copy(self.homeRotation)
        self.velocity = np.copy(self.homeVelocity)
        self.friction = np.copy(self.homeFriction)
        Object3D.updateLookAt(self)

    def setRotationY(self, value):
        self.rotation[1] = value
        self.updateLookAt()

    def updateLookAt(self):
        radianAngle = math.radians(self.rotation[1])
        # self.look[0] = self.position[0] + math.cos(radianAngle)
        # self.look[2] = self.position[2] + math.sin(radianAngle)
        # self.look[1] = self.position[1] 
        self.look[0] = math.cos(radianAngle)
        self.look[2] = math.sin(radianAngle)
        self.look[1] = 0
    
    def update(self, elapsedTime = 0):
        self.position += self.velocity
        self.updateLookAt()
    
    def intersects(self, otherObject):
        intersects = True
        for i in range(3):
            distance = math.fabs(self.position[i] - otherObject.position[i])
            radius = (self.size[0]/ 2.0 + otherObject.size[0] / 2.0)
            intersectDimension  =  distance < radius
            intersects = intersects and intersectDimension
        return intersects

    def collisionCallback(self, otherObject, initialVelocitySelf, initialVelocityOther):
        pass