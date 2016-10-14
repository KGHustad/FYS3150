import math
import numpy as np
import matplotlib.pyplot as plt

G = 4*np.pi**2

class SolarSystem:
    def __init__(self):
        self.NumberOfObjects = 0

    def CreateCelestialObject(self, x0, y0, vx0, vy0, mass, radius):
        if self.NumberOfObjects == 0:
            self.ObjectPositions = np.array( [[x0, y0]] , dtype=np.float64)
            self.ObjectVelocities = np.array( [[vx0, vy0]] , dtype=np.float64)
            self.ObjectMasses = np.array( mass , dtype=np.float64)
            self.ObjectRadiuses = np.array( radius , dtype=np.float64)
        else:
            self.ObjectPositions = np.append( self.ObjectPositions, [[x0, y0]], axis=0 )
            self.ObjectVelocities = np.append( self.ObjectVelocities, [[vx0, vy0]], axis=0 )
            self.ObjectMasses = np.append( self.ObjectMasses, mass )
            self.ObjectRadiuses = np.append( self.ObjectRadiuses, radius )
            self.AdjustSun()
        self.NumberOfObjects += 1

    def AdjustSun(self):
        "Adjust sun to ensure that the centre of mass lies in (0, 0)"
        solar_mass = self.ObjectMasses[0]
        new_celestial_object_mass = self.ObjectMasses[-1]
        mass_ratio = new_celestial_object_mass / solar_mass
        self.ObjectPositions[0,:] -= self.ObjectPositions[-1,:]*mass_ratio
        self.ObjectVelocities[0,:] -= self.ObjectVelocities[-1,:]*mass_ratio

    def ForwardEuler(self, P, V, dt):
        length = len(P)
        P_new = P
        V_new = V
        for n in xrange(length):
            V_new[n] += self.Acc(P, n, self.ObjectMasses)*dt
            P_new[n] += V_new[n]*dt
        return P_new, V_new

    def VelocityVerlet(self, P, V, dt):
        length = len(P)
        P_new = P
        V_new = V
        for n in xrange(length):
            Acc_P = self.Acc(P, n, self.ObjectMasses)
            P_new[n] = P[n] + V[n]*dt + 0.5*Acc_P*dt**2
            V_new[n] = V[n] + 0.5*(Acc_P+self.Acc(P_new, n, self.ObjectMasses))*dt
        return P_new, V_new

    def FillArray( self, steps, years ):
        num_objects = self.NumberOfObjects
        dt = float(years)/(steps+1)
        p = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        v = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        p[0] = self.ObjectPositions
        v[0] = self.ObjectVelocities
        for i in xrange( steps ):
            p[i+1], v[i+1] = self.VelocityVerlet(p[i], v[i], dt)
        return p, v

    def Acc(self, Positions, target, Masses):
        x_acc = 0
        y_acc = 0
        for i in xrange(self.NumberOfObjects):
            if i != target:
                x_distance = Positions[target,0] - Positions[i,0]
                y_distance = Positions[target,1] - Positions[i,1]
                distance = math.sqrt( x_distance**2 + y_distance**2 )
                x_acc -= G*Masses[i]*x_distance/distance**3
                y_acc -= G*Masses[i]*y_distance/distance**3
        return np.array( [x_acc, y_acc] )

    def EnergyConservation_test(self):
        self.CreateCelestialObject(0, 0, 0, 0, 1, 1)
        self.CreateCelestialObject(1, 0, 0, 2.5*np.pi, 0.0000001, 1)

        P, V = self.FillArray(100000, 15)

        KineticEnergyEarth = 0.5*self.ObjectMasses[1] * (V[:,1,0]**2 + V[:,1,1]**2) #SolarMasses*AU**2/yr**2
        KineticEnergySun = 0.5*self.ObjectMasses[0] * (V[:,0,0]**2 + V[:,0,1]**2)
        KineticEnergy = KineticEnergySun + KineticEnergyEarth

        CenterOfMass = P[:,0,:]*self.ObjectMasses[0] + P[:,1,:]*self.ObjectMasses[1]
        print CenterOfMass
        distance = np.sqrt( (P[:,1,0] - P[:,0,0])**2 + (P[:,0,1] - P[:,1,1])**2 )
        PotentialEnergy = -G*self.ObjectMasses[0]*self.ObjectMasses[1]/distance

        plt.plot(KineticEnergy)
        plt.plot(PotentialEnergy)
        plt.plot(KineticEnergy+PotentialEnergy)

        plt.show()

        AngularMomentum = self.ObjectMasses[1]*distance*np.sqrt(V[:,1,0]**2 + V[:,1,1]**2)

        plt.plot(AngularMomentum)
        plt.show()

    def TimeStep_test(self):
        self.CreateCelestialObject(0, 0, 0, 0, 1, 1)
        self.CreateCelestialObject(1, 0, 0, 2*np.pi, 0.0000001, 1)

        P10 = self.FillArray(10, 1)[0]
        P20 = self.FillArray(20, 1)[0]
        P40 = self.FillArray(40, 1)[0]
        P1000 = self.FillArray(1000, 1)[0]

        plt.plot(P10[:,1,0], P10[:,1,1], "g-")
        plt.plot(P20[:,1,0], P20[:,1,1], "r-")
        plt.plot(P40[:,1,0], P40[:,1,1], "b-")
        plt.plot(P1000[:,1,0], P1000[:,1,1], "k-")
        plt.plot(P1000[:,0,0], P1000[:,0,1], "yo")
        plt.axis([-1.5,1.5,-1.5,1.5])
        plt.title("Comparing timesteps with Forward Euler")

        plt.legend(["dt=1/10 year","dt=1/20 year","dt=1/40 year","dt=1/1000 year"])
        plt.show()
