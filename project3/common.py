import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import ctypes

G = 4*np.pi**2
c = 63197.8

class SolarSystem:
    def __init__(self):
        self.NumberOfObjects = 0

    def CreateCelestialObject(self, x0, y0, vx0, vy0, mass):
        if self.NumberOfObjects == 0:
            self.ObjectPositions = np.array( [[x0, y0]] , dtype=np.float64)
            self.ObjectVelocities = np.array( [[vx0, vy0]] , dtype=np.float64)
            self.ObjectMasses = np.array( mass , dtype=np.float64)
        else:
            self.ObjectPositions = np.append( self.ObjectPositions, [[x0, y0]], axis=0 )
            self.ObjectVelocities = np.append( self.ObjectVelocities, [[vx0, vy0]], axis=0 )
            self.ObjectMasses = np.append( self.ObjectMasses, mass )
            self.AdjustSun()
        self.NumberOfObjects += 1


    def AdjustSun(self):
        "Adjust sun to ensure that the centre of mass lies in (0, 0)"
        solar_mass = self.ObjectMasses[0]
        new_celestial_object_mass = self.ObjectMasses[-1]
        mass_ratio = new_celestial_object_mass / solar_mass
        self.ObjectPositions[0,:] -= self.ObjectPositions[-1,:]*mass_ratio
        self.ObjectVelocities[0,:] -= self.ObjectVelocities[-1,:]*mass_ratio

    def Acc(self, Positions, Velocity, target, Masses ):
        x_acc = 0
        y_acc = 0
        for i in xrange(self.NumberOfObjects):
            if i != target:
                x_distance = Positions[target,0] - Positions[i,0]
                y_distance = Positions[target,1] - Positions[i,1]
                distance = math.sqrt( x_distance**2 + y_distance**2 )
                x_acc -= G*Masses[i]*x_distance/distance**3
                y_acc -= G*Masses[i]*y_distance/distance**3
                """
                if target == 0:
                    print "Sun acc: (%15E, %15E) from %d" % (G*Masses[i]*x_distance/distance**3, G*Masses[i]*y_distance/distance**3, i)
        if target == 0:
            print "Sun acc: (%15E, %15E) TOTAL\n" % (x_acc, y_acc)
            """
        return np.array( [x_acc, y_acc] )


    def AccRelativistic(self, Positions, Velocity, target, Masses):
        x_acc = 0
        y_acc = 0
        for i in xrange(self.NumberOfObjects):
            if i != target:

                x_distance = Positions[target,0] - Positions[i,0]
                y_distance = Positions[target,1] - Positions[i,1]
                distance = math.sqrt( x_distance**2 + y_distance**2 )

                l = np.sqrt( Velocity[0]**2 + Velocity[1]**2 )
                rel_fac = 1 + ( (3*l**2) / (distance**2*c**2) )

                x_acc -= G*Masses[i]*x_distance/distance**3*rel_fac
                y_acc -= G*Masses[i]*y_distance/distance**3*rel_fac
        return np.array( [x_acc, y_acc] )

    def ForwardEuler(self, P, V, P_new, V_new, dt, acc_method):
        length = len(P)
        for n in xrange(length):
            V_new[n] = V[n] + acc_method(P, V[n], n, self.ObjectMasses)*dt
            P_new[n] = P[n] + V_new[n]*dt
        #return P, V


    def VelocityVerlet(self, P, V, P_new, V_new, dt, acc_method):
        length = len(P)
        acc_P = np.zeros((length, 2), dtype = np.float64)
        for n in xrange(length):
            acc_P[n] = acc_method(P, V[n], n, self.ObjectMasses)
            P_new[n] = P[n] + V[n]*dt + 0.5*acc_P[n]*dt**2
        for n in xrange(length):
            acc_P_new = acc_method(P_new, V[n], n, self.ObjectMasses)
            V_new[n] = V[n] + 0.5*(acc_P[n] + acc_P_new)*dt
        #return P, V


    def fill_array( self, steps, years, int_method = None, acc_method = None ):
        if int_method == None:
            int_method = self.VelocityVerlet
        if acc_method == None:
            acc_method = self.Acc
        num_objects = self.NumberOfObjects
        dt = float(years)/steps
        print "dt = %g" % dt
        p = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        v = np.zeros( shape = ( steps+1, num_objects, 2 ) )
        p[0] = self.ObjectPositions[:][:]
        v[0] = self.ObjectVelocities[:][:]

        pre = time.clock()
        for i in xrange( steps ):
            int_method(p[i], v[i], p[i+1], v[i+1], dt, acc_method)
            if i % 100 == 0 and False:
                sys.stdout.write("\r")
                sys.stdout.write("%.2f%%" % (i*100.0/steps))
                sys.stdout.flush()
        sys.stdout.write("\n")
        post = time.clock()
        time_spent = post - pre
        print "Time spent (pure Python): %g" % time_spent
        return p, v

    def fill_array_c(self, steps, years, int_method = None, acc_method = None,
                     skip_saving=None):
        if int_method == None:
            int_method = self.VelocityVerlet
        if acc_method == None:
            acc_method = self.Acc
        # only a single acc_method has been implemented yet
        integration_alg = 1 if int_method == self.VelocityVerlet else 0
        acceleration_alg = 1 if acc_method == self.AccRelativistic else 0

        num_bodies = self.NumberOfObjects
        masses = self.ObjectMasses
        dt = float(years)/steps
        if (skip_saving != 0):
            dt /= skip_saving

        p = np.zeros( shape = ( steps+1, num_bodies, 2 ), dtype=np.float64)
        v = np.zeros( shape = ( steps+1, num_bodies, 2 ), dtype=np.float64)

        p[0] = self.ObjectPositions[:][:]
        v[0] = self.ObjectVelocities[:][:]


        pre = time.clock()

        # ctypes magic
        lib_ss = np.ctypeslib.load_library("solar_system.so", "src/c")

        float64_array = np.ctypeslib.ndpointer(dtype=ctypes.c_double, ndim=1,
                                               flags="contiguous")
        lib_ss.python_interface.argstypes = [float64_array, float64_array,
                                             float64_array, ctypes.c_int,
                                             ctypes.c_int, ctypes.c_double,
                                             ctypes.c_int, ctypes.c_int,
                                             ctypes.c_int]

        lib_ss.python_interface(np.ctypeslib.as_ctypes(p),
                                np.ctypeslib.as_ctypes(v),
                                np.ctypeslib.as_ctypes(masses),
                                ctypes.c_int(num_bodies),
                                ctypes.c_int(steps),
                                ctypes.c_double(dt),
                                ctypes.c_int(skip_saving),
                                ctypes.c_int(integration_alg),
                                ctypes.c_int(acceleration_alg))

        post = time.clock()
        time_spent = post - pre
        print "Time spent (C): %g" % time_spent
        return p, v

    @staticmethod
    def EnergyConservation_test():
        TestSolarSystem = SolarSystem()
        TestSolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
        TestSolarSystem.CreateCelestialObject(1, 0, 0, 2.5*np.pi, 3.003e-6)

        P, V = TestSolarSystem.fill_array_c(100000, 15)

        KineticEnergyEarth = 0.5*TestSolarSystem.ObjectMasses[1] * (V[:,1,0]**2 + V[:,1,1]**2) #SolarMasses*AU**2/yr**2
        KineticEnergySun = 0.5*TestSolarSystem.ObjectMasses[0] * (V[:,0,0]**2 + V[:,0,1]**2)
        KineticEnergy = KineticEnergySun + KineticEnergyEarth

        CenterOfMass = P[:,0,:]*TestSolarSystem.ObjectMasses[0] + P[:,1,:]*TestSolarSystem.ObjectMasses[1]
        print CenterOfMass
        distance = np.sqrt( (P[:,1,0] - P[:,0,0])**2 + (P[:,0,1] - P[:,1,1])**2 )
        PotentialEnergy = -G*TestSolarSystem.ObjectMasses[0]*TestSolarSystem.ObjectMasses[1]/distance

        plt.plot(KineticEnergy)
        plt.plot(PotentialEnergy)
        plt.plot(KineticEnergy+PotentialEnergy)
        plt.title("Energy of Planet-Sun system over 15 years")
        plt.legend(["Kinetic Energy","Potential Energy","Total Energy"])
        plt.xlabel("time in years")
        plt.ylabel("energy in SolarMasses*AU^2/Year^2")
        plt.show()

        AngularMomentum = TestSolarSystem.ObjectMasses[1]*np.cross(P[:,1], V[:,1])
        plt.plot(AngularMomentum)
        plt.title("Angular Momentum of Planet over 15 years")
        plt.axis([0,100000,0,0.00003])
        plt.show()

    @staticmethod
    def TimeStep_test():
        TestSolarSystem = SolarSystem()
        TestSolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
        TestSolarSystem.CreateCelestialObject(1, 0, 0, 29.8*0.210805, 3.003e-6)

        P10 = TestSolarSystem.fill_array_c(10, 1)[0]
        P20 = TestSolarSystem.fill_array_c(20, 1)[0]
        P40 = TestSolarSystem.fill_array_c(40, 1)[0]
        P1000 = TestSolarSystem.fill_array_c(1000, 1)[0]

        plt.plot(P10[:,1,0], P10[:,1,1], "g-")
        plt.plot(P20[:,1,0], P20[:,1,1], "r-")
        plt.plot(P40[:,1,0], P40[:,1,1], "b-")
        plt.plot(P1000[:,1,0], P1000[:,1,1], "k-")
        plt.plot(P1000[:,0,0], P1000[:,0,1], "yo")
        plt.axis([-1.5,1.5,-1.5,1.5])
        plt.xlabel("AU")
        plt.ylabel("AU")
        plt.title("Comparing timesteps with Forward Euler")
        plt.legend(["dt=1/10 year","dt=1/20 year","dt=1/40 year","dt=1/1000 year"])
        plt.show()
