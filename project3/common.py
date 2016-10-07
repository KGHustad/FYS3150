import numpy as np
import matplotlib.pyplot as plt

G = 4*np.pi**2


class CelestialObject:
    def __init__(self, xPos, yPos, xVel, yVel, mass, radius): #All units in years and AU
        self.xPos = xPos
        self.yPos = yPos
        self.xVel = xVel
        self.yVel = yVel
        self.mass = mass
        self.radius = radius


class SolarSystem:
    def __init__(self):
        self.NumberOfObjects = 0

    def CreateObject(self, x0, y0, vx0, vy0, mass, radius):
        if NumberOfObjects = 0:
            self.ObjectPositions = np.array( (x0, y0) )
            self.ObjectVelocities = np.array( (vx0, vy0) )
            self.ObjectMasses = np.array( mass )
            self.ObjectRadiuses = np.array( radius )

    def Acc(self): #Returns an matrix with forces from and to every object
        None


    def FEulerStep(self, P, V):
        length = len(P)
        for i in range(length):
            for j in range(length):
                if i =! j:
                    p[i] +=

    def FillArray( self, steps, years, num_ojects ):
        p = np.zeros( shape = ( steps, num_ojects, 2 ) )
        v = np.zeros( shape = ( steps, num_ojects, 2 ) )

        for i in xrange( steps ):
            p[i+1], v[i+1] = self.FEulerStep(p[i], v[i])
