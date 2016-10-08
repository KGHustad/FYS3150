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

    def FEulerStep(self, P, V, dt):
        length = len(P)
        P_new = P
        V_new = V
        for n in range(length):
            V_new[n] += self.Acc(P, n, self.ObjectMasses)*dt
            P_new[n] += V_new[n]*dt
        return P_new, V_new

    def VelocityVerlet(self, P, V, dt):
        length = len(P)
        P_new = P
        V_new = V
        for n in range(length):
            Acc_P = self.Acc(P)
            P_new = P + V*dt + 0.5*Acc_P*dt**2
            V_new = V + 0.5*(Acc_P+self.Acc(P_new)*dt

    def FillArray( self, steps, years ):
        num_objects = self.NumberOfObjects
        dt = float(years)/(steps+1)
        p = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        v = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        p[0] = self.ObjectPositions
        v[0] = self.ObjectVelocities
        for i in xrange( steps ):
            p[i+1], v[i+1] = self.VelocityVerlet(p[i], v[i], dt)
        return p

    def Acc(self, Positions, target, Masses):
        x_acc = 0
        y_acc = 0
        for i in range(self.NumberOfObjects):
            if i != target:
                x_distance = Positions[target,0] - Positions[i,0]
                y_distance = Positions[target,1] - Positions[i,1]
                distance = np.sqrt( x_distance**2 + y_distance**2 )
                x_acc -= G*Masses[i]*x_distance/distance**3
                y_acc -= G*Masses[i]*y_distance/distance**3
        return np.array( [x_acc, y_acc] )

"""
    def Acc(self, p, n, s):
        return np.array([0.1,0.1])
"""
