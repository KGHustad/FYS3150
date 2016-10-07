import numpy as np
import matplotlib.pyplot as plt

G = 4*np.pi**2

"""
class CelestialObject: #Outdated
    def __init__(self, xPos, yPos, xVel, yVel, mass, radius): #All units in years and AU
        self.xPos = xPos
        self.yPos = yPos
        self.xVel = xVel
        self.yVel = yVel
        self.mass = mass
        self.radius = radius
"""

class SolarSystem:
    def __init__(self):
        self.NumberOfObjects = 0

    def CreateCelestialObject(self, x0, y0, vx0, vy0, mass, radius):
        if self.NumberOfObjects == 0:
            self.ObjectPositions = np.array( [[x0, y0]] )
            self.ObjectVelocities = np.array( [[vx0, vy0]] )
            self.ObjectMasses = np.array( mass )
            self.ObjectRadiuses = np.array( radius )
        else:
            self.ObjectPositions = np.append( self.ObjectPositions, [[x0, y0]], axis=0 )
            self.ObjectVelocities = np.append( self.ObjectVelocities, [[vx0, vy0]], axis=0 )
            self.ObjectMasses = np.append( self.ObjectMasses, mass )
            self.ObjectRadiuses = np.append( self.ObjectRadiuses, radius )
        self.NumberOfObjects += 1

    def Acc(self, Positions, target, Mass_Sources):
        x_acc = 0
        y_acc = 0
        for i in range(self.NumberOfObjects):
            if i != target:
                x_distance = abs( Positions[target,0] - Positions[i,0] )
                y_distance = abs( Positions[target,1] - Positions[i,1] )
                distance = np.sqrt( x_distance**2 + y_distance**2 )
                x_acc -= G*Mass_Sources[i]*x_distance/distance**3
                y_acc -= G*Mass_Sources[i]*y_distance/distance**3
        return np.array( x_acc, y_acc )

    def FEulerStep(self, P, V, dt):
        length = len(P)
        p_new = np.zeros( shape = (length,2) )
        v_new = np.zeros( shape = (length,2) )
        for n in range(length):
            v_new[n] += self.Acc(P, n, self.ObjectMasses)*dt
            p_new[n] += v_new[n]*dt
        return p_new, v_new

    def FillArray( self, steps, years ):
        num_objects = self.NumberOfObjects
        dt = float(years)/(steps+1)
        p = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        v = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        p[0] = self.ObjectPositions
        v[0] = self.ObjectVelocities
        print self.ObjectVelocities
        print p, v
        for i in xrange( steps ):
            p[i+1], v[i+1] = self.FEulerStep(p[i], v[i], dt)

        return p
