import math
from Object3D import *
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


class Camera(Object3D):
    def __init__(self, positionX=0, positionY=0, positionZ=0, rotationY=0, usePerspective=True, follow=None, followDistance=np.array([15.0, 5.0, 0.0], dtype=float)):
        Object3D.__init__(self, positionX=positionX, positionY=positionY,
                          positionZ=positionZ, rotationY=rotationY)
        self.homeUsePerspective = usePerspective
        self.follow = follow
        self.followDistance = followDistance
        self.reset()

    def setX(self, x):
        self.position[0] = x
        # self.updateCamera()
        self.update()

    def setY(self, y):
        self.position[1] = y
        # self.updateCamera()
        self.update()

    def setZ(self, z):
        self.position[2] = z
        # self.updateCamera()
        self.update()

    def moveForward(self, speed):
        radianAngle = math.radians(self.rotation[1])
        self.position[0] += (math.cos(radianAngle)) * speed
        self.position[2] += (math.sin(radianAngle)) * speed
        # self.updateCamera()
        self.update()

    def moveBackward(self, speed):
        radianAngle = math.radians(self.rotation[1])
        self.position[0] -= (math.cos(radianAngle)) * speed
        self.position[2] -= (math.sin(radianAngle)) * speed
        # self.updateCamera()
        self.update()

    def moveLeft(self, speed):
        radianAngle = math.radians(self.rotation[1] + 90)
        self.position[0] -= (math.cos(radianAngle)) * speed
        self.position[2] -= (math.sin(radianAngle)) * speed
        # self.updateCamera()
        self.update()

    def moveRight(self, speed):
        radianAngle = math.radians(self.rotation[1] + 90)
        self.position[0] += (math.cos(radianAngle)) * speed
        self.position[2] += (math.sin(radianAngle)) * speed
        # self.updateCamera()
        self.update()

    def moveUp(self, speed):
        self.position[1] += speed
        # self.updateCamera()
        self.update()

    def moveDown(self, speed):
        self.position[1] -= speed
        # self.updateCamera()
        self.update()

    def turnLeft(self, speed):
        self.setRotationY(self.rotation[1] - speed)

    def turnRight(self, speed):
        self.setRotationY(self.rotation[1] + speed)

    # def updateCamera(self):
    #     radianAngle = math.radians(self.rotation[1])
    #     self.look[0] = self.position[0] + math.cos(radianAngle)
    #     self.look[2] = self.position[2] + math.sin(radianAngle)
    #     self.look[1] = self.position[1]

    def reset(self):
        Object3D.reset(self)
        self.usePerspective = self.homeUsePerspective
        # self.updateCamera()
        self.update()

    def projectCamera(self):
        glLoadIdentity()
        if (self.usePerspective):
            self.setPerspectiveProjection()
        else:
            self.setOrthographicProjection()

        if (self.follow != None):
            # offset = self.follow.position - self.follow.look
            offset = np.array([-self.follow.look[0] * self.followDistance[0],
                               self.followDistance[1], -self.follow.look[2] * self.followDistance[0]])
            # obj = Object3D(positionX = self.follow.position[0] + offset[0], positionY = self.follow.position[1] + offset[1], positionZ = self.follow.position[2] + offset[2], rotationY = self.follow.rotation[1])
            gluLookAt(self.follow.position[0] + offset[0], self.follow.position[1] + offset[1], self.follow.position[2] +
                      offset[2], self.follow.position[0], self.follow.position[1] + offset[1], self.follow.position[2], 0.0, 1.0, 0.0)
        # gluLookAt(car.positionX + cameraDx, car.positionY + cameraHeight, car.positionZ + cameraDz, car.lookX, car.positionY + cameraHeight, car.lookZ, 0.0, 1.0, 0.0)
        else:
            gluLookAt(self.position[0], self.position[1], self.position[2], self.position[0] +
                      self.look[0], self.position[1] + self.look[1], self.position[2] + self.look[2], 0.0, 1.0, 0.0)
            # obj.draw()

    def setPerspectiveProjection(self):
        gluPerspective(60, 1, 1, 200)

    def setOrthographicProjection(self):
        glOrtho(-10, 10, -10, 10, 1,  200)
