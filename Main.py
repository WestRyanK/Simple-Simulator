from Camera import *
from Mailbox import *
from Car import *
from Ground import *
from Particles import *
from House import *
from KeyHandler import *
from Object3D import *
from PhysicsSimulator import *
import sys
import math
import random

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("ERROR: PyOpenGL not installed properly. ")


def init():
    glClearColor(0.0, 0.0, 0.4, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_FLAT)

def display():
    global camera
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    camera.projectCamera()
    for sceneObject in sceneObjects:
        sceneObject.draw()
    glPopMatrix()
    printText(-0.95,0.9, "Z/X - Drive car/Control camera")
    printText(-0.95,0.85, "L/K - First-person view from car/camera view")
    printText(-0.95,0.8, "A/D - Turn left/right while driving" )
    printText(-0.95,0.75, "W/S - Accelerate/brake")
    printText(-0.95,0.7, "T - Bunny hop")
    printText(-0.95,0.65, "J - Reset simulation")
    printText(-0.95, 0.6, "R/F - Shift into reverse/forward gear")
    printText(-0.95, 0.55, "H - Reset everything")
    printText(-0.95, 0.5, "O/P - Orthogonal/Perspective projection")
    printText(-0.95, 0.45, "Protip: Try running into stuff!")
    glFlush()

def printText(x, y, message):
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(x,y, 0)
    glRasterPos2f(0,0)
    for char in message:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
    glPopMatrix()

def controlCamera():
    if keyHandler.keyState[b'o']:
        camera.usePerspective = False
    if keyHandler.keyState[b'p']:
        camera.usePerspective = True
    if keyHandler.keyState[b'w']:
        camera.moveForward(speed)
    if keyHandler.keyState[b's']:
        camera.moveBackward(speed)
    if keyHandler.keyState[b'a']:
        camera.moveLeft(speed)
    if keyHandler.keyState[b'd']:
        camera.moveRight(speed)
    if keyHandler.keyState[b'r']:
        camera.moveUp(speed)
    if keyHandler.keyState[b'f']:
        camera.moveDown(speed)
    if keyHandler.keyState[b'q']:
        camera.turnLeft(speed * 2.5)
    if keyHandler.keyState[b'e']:
        camera.turnRight(speed * 2.5)

# def controlObject3D():
#     if keyHandler.keyState[b'w']:
#         objectA.velocity[0] += speed * 0.2
#     if keyHandler.keyState[b's']:
#         objectA.velocity[0] -= speed* 0.2
#     if keyHandler.keyState[b'a']:
#         objectA.velocity[2] += speed* 0.2
#     if keyHandler.keyState[b'd']:
#         objectA.velocity[2] -= speed* 0.2
#     if keyHandler.keyState[b't'] and objectA.position[1] <= 0:
#         objectA.velocity[1] += speed * 1

def controlCar():
    global car
    if keyHandler.keyState[b'w']:
        car.accelerate()
    if keyHandler.keyState[b's']:
        car.brake()
    if keyHandler.keyState[b'a']:
        car.turnLeft()
    if keyHandler.keyState[b'd']:
        car.turnRight()
    if keyHandler.keyState[b'r']:
        car.isBackingUp = True
    if keyHandler.keyState[b'f']:
        car.isBackingUp = False
    if keyHandler.keyState[b't'] and car.position[1] <= 0:
        car.velocity[1] += speed  * 1.2

def handleInput():
    global keyState
    global physicsSimulator
    global isControlObject
    global isControlCar
    if keyHandler.keyState[chr(27)]:
        import sys
        sys.exit(0)

    # if (isControlObject):
    #     controlObject3D()
    if (isControlCar):
        controlCar()
    else:
        controlCamera()

    # if (keyHandler.keyState[b'c']):
    #     isControlObject = True
    #     isControlCar = False
    if (keyHandler.keyState[b'x']):
        isControlObject = False
        isControlCar = False
    if (keyHandler.keyState[b'z']):
        isControlCar = True
        isControlObject = False
    if (keyHandler.keyState[b'l']):
        camera.follow = car
    if (keyHandler.keyState[b'k']):
        camera.follow = None
    if keyHandler.keyState[b'j']:
        for sceneObject in sceneObjects:
            sceneObject.reset()
        figure8Timer = 0
    if keyHandler.keyState[b'h']:
        for sceneObject in sceneObjects:
            sceneObject.reset()
        camera.reset()
        figure8Timer = 0
    if keyHandler.keyState[b'o']:
        camera.usePerspective = False
    if keyHandler.keyState[b'p']:
        camera.usePerspective = True

def update(elapsedTime):
    global physicsSimulator
    handleInput()
    animate(elapsedTime)
    physicsSimulator.simulatePhysics(elapsedTime, sceneObjects)
    glutPostRedisplay()
    glutTimerFunc(elapsedTime, update, elapsedTime)
    # print camera.position
    # print camera.rotation[1]

figure8Timer = 0
figure8Switch = 2000
def animate(elapsedTime):
    global figure8Timer
    global figure8Switch
    global car2
    global car3
    global car4
    figure8Timer += elapsedTime
    if (figure8Timer > figure8Switch):
        figure8Timer = figure8Timer % figure8Switch
        car2.steeringAngle = -car2.steeringAngle
    car2.accelerate()
    if (magnitude(car3.position) > 200):
        car3.reset()
    if (magnitude(car4.position) > 200):
        car4.reset()
    car3.accelerate()
    car4.accelerate()


camera = Camera(-9, 4, -26, 70)
physicsSimulator = PhysicsSimulator()
physicsSimulator.simulate = True
isControlCar = False

sceneObjects = []
car = Car(positionZ = 20, rotationY = 0)
# car.mass = 15
sceneObjects.append(car)
ground = Ground()
sceneObjects.append(ground)
sceneObjects.extend(generateNeighborhood())
car2 = Car(positionZ = 40, positionX = -20, steeringAngle = 10)
sceneObjects.append(car2)
car3 = Car(positionZ = 11, positionX = -40, driveAcceleration=0.06)
car3.mass = 15
sceneObjects.append(car3)
car4 = Car(positionZ = 11, positionX = 40, rotationY = 180, driveAcceleration=0.06)
sceneObjects.append(car4)
car4.mass = 15
sceneObjects.extend(generateMailboxes())
DISPLAY_WIDTH = 800.0
DISPLAY_HEIGHT = 800.0
updateFPS = 1000 / 30
simulationSlowdown = 4000.0
speed = 1
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition(660, 100)
glutCreateWindow(b'OpenGL Lab')
init()
glutDisplayFunc(display)
keyHandler = KeyHandler()
glutTimerFunc(updateFPS, update, updateFPS)
glutMainLoop()