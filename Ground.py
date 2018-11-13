from Object3D import *
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Ground(Object3D):

    def __init__(self): 
        Object3D.__init__(self)
        self.checkCollisions = False
    
    def drawLines(self, count, spacing, angle, x, z):
        glColor3f(1,1,0)
        w = 0.3
        l = 1.5
        glPushMatrix()
        glTranslatef(x, 0, z)
        glRotatef(angle, 0,1,0)
        for i in range(count):
            glPushMatrix()
            glTranslatef(i * spacing, 0, 0)
            glBegin(GL_QUADS)
            glVertex3f(l, 0.02, w)
            glVertex3f(l, 0.02, -w)
            glVertex3f(-l, 0.02, -w)
            glVertex3f(-l, 0.02, w)
            glEnd()
            glPopMatrix()
        glPopMatrix()

    def drawObject(self):
        glLineWidth(2.5)
        glColor3f(0.0, 0.4, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(-1000, 0, -1000)
        glVertex3f(1000, 0, -1000)
        glVertex3f(1000, 0, 1000)
        glVertex3f(-1000, 0, 1000)

        glColor3f(0.4, 0.4, 0.4)
        glVertex3f(-1000, 0.01, -15)
        glVertex3f(-1000, 0.01, 15)
        glVertex3f(1000, 0.01, -15)
        glVertex3f(1000, 0.01, 15)

        glVertex3f(-15, 0.01, -1000)
        glVertex3f(15, 0.01, -1000)
        glVertex3f(-15, 0.01, 1000)
        glVertex3f(15, 0.01, 1000)
        glEnd()

        self.drawLines(40, 5, 0, 15, 7.5)
        self.drawLines(40, 5, 180, -3, 7.5)
        self.drawLines(40, 5, -90, 7.5, 16)
        self.drawLines(40, 5, 90, 7.5, -1)