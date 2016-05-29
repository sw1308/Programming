import time
import math

class GravitationalBody(object):
    """Object that obeys the laws of gravity, all objects are circular and their mass is equal to their area."""
    def __init__(self, radius, xPos, yPos, xSpeed, ySpeed):
        """
        radius      -   radius of the object (should be int for efficiency).
        mass        -   mass of the object, equal to pi*(radius**2)
        xPos        -   starting x position of the object
        yPos        -   starting y position of the object
        xSpeed      -   starting speed along the x axis for the object
        ySpeed      -   starting speed along the y axis for the object
        lastUpdated -   keeps track of the time per step to maintain accuracy.
                        Note that it is used as a fallback measure and would lead
                        to innefficiencies if used with multiple objects. Is is
                        recommended to call updatePos() after calculating the
                        timeDelta yourself to avoid multiple calls.
        """

        super(GravitationalBody, self).__init__()
        self.radius = float(radius)
        self.mass = math.pi * (radius ** 2) * 1000000000000 # Multiply manyfold to make reasonable gForce
        self.xPos = float(xPos)
        self.yPos = float(yPos)
        self.xSpeed = float(xSpeed) # Change per step
        self.ySpeed = float(ySpeed) # Change per step
        self.lastUpdated = time.time()
        self.physicsless = False # Used to prevent acceleration

    def getVelocity(self): # Returns a vector
        return (self.xSpeed, self.ySpeed)

    def exertForce(self, force, timeDelta): # Expects force to be a 2D vector of floats
        if not self.physicsless:
            self.xSpeed = self.xSpeed + (force[0] / self.mass) * timeDelta
            self.ySpeed = self.ySpeed + (force[1] / self.mass) * timeDelta

    def updatePos(self, timeDelta=None): # Applies it's velocity to it's current position taking into account the time since the last update
        if timeDelta is None:
            # Must calculate the amount of time since last updated
            currentTime = time.time()
            timeDelta = currentTime - self.lastUpdated
            self.lastUpdated = currentTime

        else:
            # Prepare lastUpdated in case next update doesn't supply timeDelta
            self.lastUpdated += timeDelta

        self.xPos += self.xSpeed * timeDelta
        self.yPos += self.ySpeed * timeDelta