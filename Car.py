import math
from Particles import *
import random
from Object3D import *
from Util3D import *

class Car(Object3D):
    def __init__(self, positionX = 0, positionZ = 0, rotationY = 0, driveAcceleration = 0.2, brakeAcceleration = 0.2, maxSpeed = 6, isBackingUp = False, steeringAngle = 0, maxSteeringAngle = 15):
        radianAngle = math.radians(rotationY)
        Object3D.__init__(self, positionX = positionX, positionZ = positionZ, rotationY = rotationY, frictionX = 0.0002, frictionZ = 0.005)
        self.homeDriveAcceleration = driveAcceleration
        self.homeBrakeAcceleration = brakeAcceleration
        self.homeMaxSpeed = maxSpeed
        self.checkCollisions = True
        self.homeIsBackingUp = isBackingUp
        self.homeSteeringAngle = steeringAngle
        self.homeMaxSteeringAngle = maxSteeringAngle
        self.steeringAngleChange = 2.0
        self.mass = 10
        self.bumperInset = 0.2 + random.random() * 0.4
        self.roofInset = 0.2 + random.random() * 0.4
        self.carLift = 1.5
        self.doorHeight = random.random() * 0.75 + 0.5
        self.bodyHeight = random.random() + 1.75
        self.paintR = random.random()
        self.paintG = random.random()
        self.paintB = random.random()
        self.particles = Particles()
        self.particles.emit = False
        length = random.random() + 5.5
        width = random.random() + 3.5
        self.size = np.array([length, self.carLift + self.bodyHeight, width], dtype=float)
        self.reset()

    def reset(self):
        Object3D.reset(self)
        self.driveAcceleration = self.homeDriveAcceleration
        self.brakeAcceleration = self.homeBrakeAcceleration
        self.maxSpeed = self.homeMaxSpeed
        self.isBackingUp = self.homeIsBackingUp
        self.isBraking = True
        self.steeringAngle = self.homeSteeringAngle
        self.maxSteeringAngle = self.homeMaxSteeringAngle
        self.tireRotation = 0
        self.particles.reset()
    
    def collisionCallback(self, otherObject, initialVelocitySelf, initialVelocityOther):
        speed = magnitude(initialVelocitySelf - initialVelocityOther) * 0.1
        self.velocity[1] = min(0.4, speed)
        self.particles.reset()
        impactPoint =  self.position - ((self.position + otherObject.position) / 2.0) 
        self.particles.emitting = True
        self.update()

    def accelerate(self):
        self.isBraking = self.isBackingUp
        if (self.position[1] <= 0):
            if not self.isBackingUp:
                self.velocity[0] +=  self.look[0] * self.driveAcceleration
                self.velocity[2] += self.look[2] * self.driveAcceleration
            else:
                self.velocity[0] -=  self.look[0] * self.driveAcceleration
                self.velocity[2] -= self.look[2] * self.driveAcceleration


    def brake(self):
        self.isBraking = True
        if (self.position[1] <= 0):
            brake = self.look * self.brakeAcceleration
            if (magnitude(self.velocity) < magnitude(brake)):
                self.velocity[0] = 0
                self.velocity[1] = 0
                self.velocity[2] = 0
            else:
                self.velocity -= brake

    def turnLeft(self):
        if (self.isBackingUp == False):
            self.isBraking = False
        if (math.fabs(self.steeringAngle) < 4):
            self.steeringAngle += self.steeringAngleChange * 0.25
        else:
            self.steeringAngle += self.steeringAngleChange
        if (self.steeringAngle > self.maxSteeringAngle):
            self.steeringAngle = self.maxSteeringAngle

    def turnRight(self):
        if (self.isBackingUp == False):
            self.isBraking = False
        if (math.fabs(self.steeringAngle) < 4):
            self.steeringAngle -= self.steeringAngleChange * 0.25
        else:
            self.steeringAngle -= self.steeringAngleChange
        if (self.steeringAngle < -self.maxSteeringAngle):
            self.steeringAngle = -self.maxSteeringAngle

    def update(self, elapsedTime = 0):
        changeAngle = self.steeringAngle * magnitude(self.velocity) * 0.5
        speedForward = self.look.dot(self.velocity)
        self.tireRotation -= speedForward * 15
        if (not self.isBackingUp):
            self.rotation[1] -= changeAngle
            self.updateLookAt()
        else:
            self.rotation[1] += changeAngle
            self.updateLookAt()
        self.particles.update(elapsedTime)
        Object3D.update(self)


    def drawObject(self):
        glPushMatrix()
        self.particles.draw()
        glRotate(-self.rotation[1], 0.0, 1.0, 0.0)
        glPopMatrix()
        carWidth = self.size[2] * 0.5
        carLength = self.size[0] * 0.5
        bumperWidth = carWidth - self.bumperInset
        tireLocation = carLength - 1.5
        ls = 0.2 # light size
        self.drawTireInstance(self.tireRotation, tireLocation, 1, carWidth, self.steeringAngle)
        self.drawTireInstance(self.tireRotation, tireLocation, 1, -carWidth, self.steeringAngle)
        self.drawTireInstance(self.tireRotation, -tireLocation, 1, carWidth)
        self.drawTireInstance(self.tireRotation, -tireLocation, 1, -carWidth)
        
        headR = 1
        headG = 1
        headB = 0.5
        if (self.isBraking or self.isBackingUp):
            tailR = 1
            tailG = 0
            tailB = 0
        else:
            tailR = 0.5
            tailG = 0.5
            tailB = 0.5
        self.drawLight(headR, headG, headB, carLength + .01, self.carLift + ls*2, bumperWidth - ls*2, ls)
        self.drawLight(headR, headG, headB, carLength + .01, self.carLift + ls*2, -bumperWidth + ls*2, ls)
        self.drawLight(tailR, tailG, tailB, -carLength - .01, self.carLift + ls*2, bumperWidth - ls*2, ls)
        self.drawLight(tailR, tailG, tailB, -carLength - .01, self.carLift + ls*2, -bumperWidth + ls*2, ls)
        self.drawCarBody()

    def drawTireInstance(self, tireRotation = 0, tireX = 0, tireY = 0, tireZ = 0, steeringAngle = 0):
        glPushMatrix()
        glTranslatef(tireX, tireY, tireZ)
        glRotatef(steeringAngle, 0, 1, 0)
        glRotatef(tireRotation, 0, 0, 1)
        self.drawTire()
        glPopMatrix()
    
    def drawBreakLight(self, x = 0, y = 0, z = 0):
        glPushMatrix()
        glTranslatef(x, y, z)
        self.drawRedLight(self.isBraking)
        glPopMatrix()
    
    def drawLight(self, r,g,b, x, y, z, size):
        s = size
        glPushMatrix()
        glTranslatef(x,y,z)
        glColor3f(r,g,b)
        glBegin(GL_QUADS)
        glVertex3f(0, -s, -s)
        glVertex3f(0, s, -s)
        glVertex3f(0, s, s)
        glVertex3f(0, -s, s)
        glEnd()
        glPopMatrix()

    def drawCarBody(self):
        w = self.size[2] * 0.5 # car width
        rw = w - self.roofInset # rear window width
        fb = w - self.bumperInset # front bumper width
        li = self.carLift
        dh = self.doorHeight + li
        h = self.size[1]
        l = self.size[0] * 0.5
        wi = l - 1
        glLineWidth(2.5)
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.2, 0.2)
        # back windshield
        glVertex3f(-l,dh,fb)
        glVertex3f(-wi,h,rw)
        glVertex3f(-wi,h,-rw)
        glVertex3f(-l,dh,-fb)

        # front windshield
        glVertex3f(l,dh,fb)
        glVertex3f(wi,h,rw)
        glVertex3f(wi,h,-rw)
        glVertex3f(l,dh,-fb)

        # right window
        glVertex3f(wi,dh,w)
        glVertex3f(-wi,dh,w)
        glVertex3f(-wi,h,rw)
        glVertex3f(wi,h,rw)

        # left window
        glVertex3f(wi,dh,-w)
        glVertex3f(-wi,dh,-w)
        glVertex3f(-wi,h,-rw)
        glVertex3f(wi,h,-rw)

        # trunk
        glColor3f(self.paintR, self.paintG, self.paintB)
        glVertex3f(-l,dh,fb)
        glVertex3f(-l,li,fb)
        glVertex3f(-l,li,-fb)
        glVertex3f(-l,dh,-fb)

        # front bumper
        glVertex3f(l,dh,fb)
        glVertex3f(l,li,fb)
        glVertex3f(l,li,-fb)
        glVertex3f(l,dh,-fb)

        # roof
        glVertex3f(-wi,h,-rw)
        glVertex3f(wi,h,-rw)
        glVertex3f(wi,h,rw)
        glVertex3f(-wi,h,rw)

        # back right panel
        glVertex3f(-wi,dh,w)
        glVertex3f(-l,dh,fb)
        glVertex3f(-l,li,fb)
        glVertex3f(-wi,li,w)

        # front right panel
        glVertex3f(wi,dh,w)
        glVertex3f(l,dh,fb)
        glVertex3f(l,li,fb)
        glVertex3f(wi,li,w)

        # back left panel
        glVertex3f(-wi,dh,-w)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-l,li,-fb)
        glVertex3f(-wi,li,-w)

        # front left panel
        glVertex3f(wi,dh,-w)
        glVertex3f(l,dh,-fb)
        glVertex3f(l,li,-fb)
        glVertex3f(wi,li,-w)

        # right sidepanel
        glVertex3f(wi,dh,w)
        glVertex3f(-wi,dh,w)
        glVertex3f(-wi,li,w)
        glVertex3f(wi,li,w)

        # left sidepanel
        glVertex3f(wi,dh,-w)
        glVertex3f(-wi,dh,-w)
        glVertex3f(-wi,li,-w)
        glVertex3f(wi,li,-w)

        glEnd()

        glBegin(GL_TRIANGLES)
        # back right top panel
        glVertex3f(-wi,h,rw)
        glVertex3f(-l,dh,fb)
        glVertex3f(-wi,dh,w)

        # back left top panel
        glVertex3f(-wi,h,-rw)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-wi,dh,-w)

        # front right top panel
        glVertex3f(wi,h,rw)
        glVertex3f(l,dh,fb)
        glVertex3f(wi,dh,w)

        # front left top panel
        glVertex3f(wi,h,-rw)
        glVertex3f(l,dh,-fb)
        glVertex3f(wi,dh,-w)
        glEnd()


        glLineWidth(2.5)
        glColor3f(0,0,0)
        glBegin(GL_LINES)
        # back windshield
        glVertex3f(-l,dh,fb)
        glVertex3f(-wi,h,rw)
        glVertex3f(-wi,h,rw)
        glVertex3f(-wi,h,-rw)
        glVertex3f(-wi,h,-rw)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-l,dh,fb)

        # front windshield
        glVertex3f(l,dh,fb)
        glVertex3f(wi,h,rw)
        glVertex3f(wi,h,rw)
        glVertex3f(wi,h,-rw)
        glVertex3f(wi,h,-rw)
        glVertex3f(l,dh,-fb)
        glVertex3f(l,dh,-fb)
        glVertex3f(l,dh,fb)

        # right window
        glVertex3f(wi,dh,w)
        glVertex3f(-wi,dh,w)
        glVertex3f(-wi,dh,w)
        glVertex3f(-wi,h,rw)
        glVertex3f(-wi,h,rw)
        glVertex3f(wi,h,rw)
        glVertex3f(wi,h,rw)
        glVertex3f(wi,dh,w)

        # left window
        glVertex3f(wi,dh,-w)
        glVertex3f(-wi,dh,-w)
        glVertex3f(-wi,dh,-w)
        glVertex3f(-wi,h,-rw)
        glVertex3f(-wi,h,-rw)
        glVertex3f(wi,h,-rw)
        glVertex3f(wi,h,-rw)
        glVertex3f(wi,dh,-w)

        # trunk
        glVertex3f(-l,dh,fb)
        glVertex3f(-l,li,fb)
        glVertex3f(-l,li,fb)
        glVertex3f(-l,li,-fb)
        glVertex3f(-l,li,-fb)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-l,dh,fb)

        # front bumper
        glVertex3f(l,dh,fb)
        glVertex3f(l,li,fb)
        glVertex3f(l,li,fb)
        glVertex3f(l,li,-fb)
        glVertex3f(l,li,-fb)
        glVertex3f(l,dh,-fb)
        glVertex3f(l,dh,-fb)
        glVertex3f(l,dh,fb)

        # back right panel
        glVertex3f(-wi,dh,w)
        glVertex3f(-l,dh,fb)
        glVertex3f(-l,dh,fb)
        glVertex3f(-l,li,fb)
        glVertex3f(-l,li,fb)
        glVertex3f(-wi,li,w)
        glVertex3f(-wi,li,w)
        glVertex3f(-wi,dh,w)

        # front right panel
        glVertex3f(wi,dh,w)
        glVertex3f(l,dh,fb)
        glVertex3f(l,dh,fb)
        glVertex3f(l,li,fb)
        glVertex3f(l,li,fb)
        glVertex3f(wi,li,w)
        glVertex3f(wi,li,w)
        glVertex3f(wi,dh,w)

        # back left panel
        glVertex3f(-wi,dh,-w)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-l,dh,-fb)
        glVertex3f(-l,li,-fb)
        glVertex3f(-l,li,-fb)
        glVertex3f(-wi,li,-w)
        glVertex3f(-wi,li,-w)
        glVertex3f(-wi,dh,-w)

        # front left panel
        glVertex3f(wi,dh,-w)
        glVertex3f(l,dh,-fb)
        glVertex3f(l,dh,-fb)
        glVertex3f(l,li,-fb)
        glVertex3f(l,li,-fb)
        glVertex3f(wi,li,-w)
        glVertex3f(wi,li,-w)
        glVertex3f(wi,dh,-w)

        glVertex3f(-wi,li,-w)
        glVertex3f(wi,li,-w)
        glVertex3f(-wi,li,w)
        glVertex3f(wi,li,w)
        glEnd()
        
    def drawTire(self):
        glLineWidth(2.5)
        glBegin(GL_QUADS)
        glColor3f(0.2,0.2,0.2)
        glVertex3f(-1, .5, .5)
        glVertex3f(-1, .5, -.5)
        glVertex3f(-.5, 1, -.5)
        glVertex3f(-.5, 1, .5)

        glVertex3f(-.5, 1, -.5)
        glVertex3f(-.5, 1, .5)
        glVertex3f(.5, 1, .5)
        glVertex3f(.5, 1, -.5)

        glVertex3f(.5, 1, .5)
        glVertex3f(.5, 1, -.5)
        glVertex3f(1, .5, -.5)
        glVertex3f(1, .5, .5)

        glVertex3f(1, .5, -.5)
        glVertex3f(1, .5, .5)
        glVertex3f(1, -.5, .5)
        glVertex3f(1, -.5, -.5)

        glVertex3f(1, -.5, .5)
        glVertex3f(1, -.5, -.5)
        glVertex3f(.5, -1, -.5)
        glVertex3f(.5, -1, .5)

        glVertex3f(.5, -1, -.5)
        glVertex3f(.5, -1, .5)
        glVertex3f(-.5, -1, .5)
        glVertex3f(-.5, -1, -.5)

        glVertex3f(-.5, -1, .5)
        glVertex3f(-.5, -1, -.5)
        glVertex3f(-1, -.5, -.5)
        glVertex3f(-1, -.5, .5)

        glVertex3f(-1, -.5, -.5)
        glVertex3f(-1, -.5, .5)
        glVertex3f(-1, .5, .5)
        glVertex3f(-1, .5, -.5)

        glColor3f(0.9, 0.9, 0.9)
        glVertex3f(-1, .5, -.5)
        glVertex3f(-.5, 1, -.5)
        glVertex3f(-.5, -1, -.5)
        glVertex3f(-1, -.5, -.5)

        glVertex3f(1, .5, -.5)
        glVertex3f(.5, 1, -.5)
        glVertex3f(.5, -1, -.5)
        glVertex3f(1, -.5, -.5)

        glVertex3f(-.5, 1, -.5)
        glVertex3f(-.5, -1, -.5)
        glVertex3f(.5, -1, -.5)
        glVertex3f(.5, 1, -.5)

        glVertex3f(-1, .5, .5)
        glVertex3f(-.5, 1, .5)
        glVertex3f(-.5, -1, .5)
        glVertex3f(-1, -.5, .5)

        glVertex3f(1, .5, .5)
        glVertex3f(.5, 1, .5)
        glVertex3f(.5, -1, .5)
        glVertex3f(1, -.5, .5)

        glVertex3f(-.5, 1, .5)
        glVertex3f(-.5, -1, .5)
        glVertex3f(.5, -1, .5)
        glVertex3f(.5, 1, .5)
        glEnd()
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        #Front Side
        glVertex3f(-1, .5, .5)
        glVertex3f(-.5, 1, .5)
        glVertex3f(-.5, 1, .5)
        glVertex3f(.5, 1, .5)
        glVertex3f(.5, 1, .5)
        glVertex3f(1, .5, .5)
        glVertex3f(1, .5, .5)
        glVertex3f(1, -.5, .5)
        glVertex3f(1, -.5, .5)
        glVertex3f(.5, -1, .5)
        glVertex3f(.5, -1, .5)
        glVertex3f(-.5, -1, .5)
        glVertex3f(-.5, -1, .5)
        glVertex3f(-1, -.5, .5)
        glVertex3f(-1, -.5, .5)
        glVertex3f(-1, .5, .5)
        #Back Side
        glVertex3f(-1, .5, -.5)
        glVertex3f(-.5, 1, -.5)
        glVertex3f(-.5, 1, -.5)
        glVertex3f(.5, 1, -.5)
        glVertex3f(.5, 1, -.5)
        glVertex3f(1, .5, -.5)
        glVertex3f(1, .5, -.5)
        glVertex3f(1, -.5, -.5)
        glVertex3f(1, -.5, -.5)
        glVertex3f(.5, -1, -.5)
        glVertex3f(.5, -1, -.5)
        glVertex3f(-.5, -1, -.5)
        glVertex3f(-.5, -1, -.5)
        glVertex3f(-1, -.5, -.5)
        glVertex3f(-1, -.5, -.5)
        glVertex3f(-1, .5, -.5)
        #Connectors
        glVertex3f(-1, .5, .5)
        glVertex3f(-1, .5, -.5)
        glVertex3f(-.5, 1, .5)
        glVertex3f(-.5, 1, -.5)
        glVertex3f(.5, 1, .5)
        glVertex3f(.5, 1, -.5)
        glVertex3f(1, .5, .5)
        glVertex3f(1, .5, -.5)
        glVertex3f(1, -.5, .5)
        glVertex3f(1, -.5, -.5)
        glVertex3f(.5, -1, .5)
        glVertex3f(.5, -1, -.5)
        glVertex3f(-.5, -1, .5)
        glVertex3f(-.5, -1, -.5)
        glVertex3f(-1, -.5, .5)
        glVertex3f(-1, -.5, -.5)
        glEnd()