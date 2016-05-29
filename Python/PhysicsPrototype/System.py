#! /usr/bin/python

import time
import math
import unittest
import GravitationalBody
import GrafixFrontEnd as frontEnd

timeStep = 1

G = 6.67408e-11 # Gravitational constant
xSize = frontEnd.screenSize[0]
ySize = frontEnd.screenSize[1]

def calculateDistance(object1, object2):
    # Pythagorean theorem to calculate straight line distance between centre of two objects
    return math.sqrt(((object2.xPos - object1.xPos) ** 2) + ((object2.yPos - object1.yPos) ** 2))

def calculateGForce(object1, object2):
    # F = G((m1*m2)/r^2)
    distance = calculateDistance(object1, object2)
    differenceVector = (object2.xPos - object1.xPos, object2.yPos - object1.yPos)
    tempForce = -G * ((object1.mass * object2.mass) / (distance ** 2))

    return (tempForce * normalizeVector(differenceVector)[0], tempForce * normalizeVector(differenceVector)[1])

def normalizeVector(vector):
    norm = []
    unitVector = math.sqrt(math.fsum(component**2 for component in vector)) # Calculate the unit vector using the components of the vector argument

    for component in vector:
        norm.append(component / unitVector)

    return tuple(norm)

def getAllPermutations(objects):
    currentPos = 0
    length = len(objects)
    returnList = []

    while currentPos < length - 1:
        for i in xrange(currentPos + 1, length):
            returnList.append((objects[currentPos], objects[i]))

        currentPos += 1

    return returnList

# Detects collisions and objects leaving the screen and acts appropriately
def detectCollisions(objects):

    # Detect collisions between objects
    for obj1, obj2 in getAllPermutations(objects):
        acceptableDistance = obj1.radius + obj2.radius
        actualDistance = calculateDistance(obj1, obj2)

        if actualDistance < acceptableDistance:
            # Current code just prevents objects from being affected by gravity
            # causing them to phase through each other unaffected.
            obj1.physicsless = True
            obj2.physicsless = True

        elif obj1.physicsless and obj2.physicsless:
            obj1.physicsless = False
            obj2.physicsless = False

    # Detect collisions with edge of window
    for obj in objects:
        if obj.xPos > xSize:
            obj.xPos = 1
        elif obj.xPos < 1:
            obj.xPos = xSize - 1

        if obj.yPos > ySize:
            obj.yPos = 1
        elif obj.yPos < 1:
            obj.yPos = ySize - 1

def simulate(objects):
    oldTime = time.time()
    finished = False

    while not finished:
        currentTime = time.time()

        timeDelta = (currentTime - oldTime) * timeStep

        for obj1, obj2 in getAllPermutations(objects):
            gForce = calculateGForce(obj1, obj2) # Returns force experienced by obj2

            obj2.exertForce(gForce, timeDelta)

            # Flip the gForce before applying it to the other object
            gForce = (-gForce[0], -gForce[1])

            obj1.exertForce(gForce, timeDelta)

        for obj in objects:
            obj.updatePos(currentTime - oldTime)

        detectCollisions(objects)

        finished = frontEnd.renderOnce(objects, finished)

        oldTime = currentTime

    frontEnd.renderOnce(objects, finished) # Allow graphical front-end to quit appropriately

class testSystem(unittest.TestCase):
    def testGetAllPermutations(self):
        testList = [0,1,2,3,4,5]

        self.assertEqual(getAllPermutations(testList),
            [
                (0,1),
                (0,2),
                (0,3),
                (0,4),
                (0,5),
                (1,2),
                (1,3),
                (1,4),
                (1,5),
                (2,3),
                (2,4),
                (2,5),
                (3,4),
                (3,5),
                (4,5)
            ]
        )

    def testNormalizeVector(self):
        testVector = (5, 5)

        self.assertEqual(normalizeVector(testVector),
            (0.7071067811865475, 0.7071067811865475) # Value given by online calculator was 0.707107 however after hand checking I verified that this was the result of rounding the output.
        )

    def testCalculateDistance(self):
        testObj1 = GravitationalBody.GravitationalBody(20, 50, 0, 0, 0)
        testObj2 = GravitationalBody.GravitationalBody(20, 0, 50, 0, 0)

        self.assertEqual(calculateDistance(testObj1, testObj2), 70.71067811865476)

    def testCalculateGForce(self):
        testObj1 = GravitationalBody.GravitationalBody(20, 50, 0, 0, 0)
        testObj2 = GravitationalBody.GravitationalBody(20, 0, 50, 0, 0)

        self.assertEqual(calculateGForce(testObj1, testObj2), (1.490479935280827e+16, -1.490479935280827e+16))

if __name__ == '__main__':
    # unittest.main()

    objectList = [
        # GravitationalBody.GravitationalBody(10, 600, 500, 0, 5),
        # GravitationalBody.GravitationalBody(10, 400, 500, 0, -5),
        GravitationalBody.GravitationalBody(100, 500, 500, 0, 0),
        GravitationalBody.GravitationalBody(10, 700, 500, 0, 100),
        GravitationalBody.GravitationalBody(10, 300, 500, 0, -100),
        GravitationalBody.GravitationalBody(10, 500, 800, 100, 0)
        # GravitationalBody.GravitationalBody(10, 20, 150, 0, 1),
        # GravitationalBody.GravitationalBody(10, 300, 300, 1, 0),
        # GravitationalBody.GravitationalBody(10, 400, 250, 0, 0),
        # GravitationalBody.GravitationalBody(10, 450, 400, 1, 0)
    ]

    simulate(objectList)
