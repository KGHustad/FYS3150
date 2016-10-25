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

    def CreateCelestialObject(self, x0, y0, vx0, vy0, mass, adjust_sun=True):
        if self.NumberOfObjects == 0:
            self.ObjectPositions = np.array( [[x0, y0]] , dtype=np.float64)
            self.ObjectVelocities = np.array( [[vx0, vy0]] , dtype=np.float64)
            self.ObjectMasses = np.array( mass , dtype=np.float64)
        else:
            self.ObjectPositions = np.append( self.ObjectPositions, [[x0, y0]], axis=0 )
            self.ObjectVelocities = np.append( self.ObjectVelocities, [[vx0, vy0]], axis=0 )
            self.ObjectMasses = np.append( self.ObjectMasses, mass )
            if adjust_sun:
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
        "Classical acceleration"
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


    def AccRelativistic(self, Positions, Velocity, target, Masses):
        "Relativistic acceleration"
        x_acc = 0
        y_acc = 0
        for i in xrange(self.NumberOfObjects):
            if i != target:

                x_distance = Positions[target,0] - Positions[i,0]
                y_distance = Positions[target,1] - Positions[i,1]
                distance = math.sqrt( x_distance**2 + y_distance**2 )

                l = math.sqrt( Velocity[0]**2 + Velocity[1]**2 )
                rel_fac = 1 + ( (3*l**2) / (distance**2*c**2) )

                x_acc -= G*Masses[i]*x_distance/distance**3*rel_fac
                y_acc -= G*Masses[i]*y_distance/distance**3*rel_fac
        return np.array( [x_acc, y_acc] )

    def ForwardEuler(self, P, V, P_new, V_new, dt, acc_method):
        length = len(P)
        for n in xrange(length):
            P_new[n] = P[n] + V[n]*dt
            V_new[n] = V[n] + acc_method(P, V[n], n, self.ObjectMasses)*dt


    def VelocityVerlet(self, P, V, P_new, V_new, dt, acc_method):
        length = len(P)
        acc_P = np.zeros((length, 2), dtype = np.float64)
        for n in xrange(length):
            acc_P[n] = acc_method(P, V[n], n, self.ObjectMasses)
            P_new[n] = P[n] + V[n]*dt + 0.5*acc_P[n]*dt**2
        for n in xrange(length):
            acc_P_new = acc_method(P_new, V[n], n, self.ObjectMasses)
            V_new[n] = V[n] + 0.5*(acc_P[n] + acc_P_new)*dt

    def EulerCromer(self, P, V, P_new, V_new, dt, acc_method):
        length = len(P)
        for n in xrange(length):
            V_new[n] = V[n] + acc_method(P, V[n], n, self.ObjectMasses)*dt
            P_new[n] = P[n] + V_new[n]*dt


    def fill_array(self, steps, years, int_method = None, acc_method = None,
                   silent=False):
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
        if not silent:
            print "Time spent (pure Python): %g" % time_spent
        return p, v

    def fill_array_c(self, steps, years, int_method = None, acc_method = None,
                     skip_saving=0, silent=False, perihelion_minima=0):
        if int_method == None:
            int_method = self.VelocityVerlet
        if acc_method == None:
            acc_method = self.Acc

        int_methods = [self.ForwardEuler, self.VelocityVerlet,
                       self.EulerCromer]
        acc_methods = [self.Acc, self.AccRelativistic]

        integration_alg = int_methods.index(int_method)
        acceleration_alg = acc_methods.index(acc_method)

        # minima for perihelion
        minima = np.zeros(shape=(perihelion_minima, 6), dtype=np.float64)

        num_bodies = self.NumberOfObjects
        masses = self.ObjectMasses
        dt = float(years)/steps
        if (skip_saving != 0):
            dt /= skip_saving

        p = np.empty( shape = ( steps+1, num_bodies, 2 ), dtype=np.float64)
        v = np.empty( shape = ( steps+1, num_bodies, 2 ), dtype=np.float64)

        p[0] = self.ObjectPositions[:][:]
        v[0] = self.ObjectVelocities[:][:]


        pre = time.clock()

        # ctypes magic
        lib_ss = np.ctypeslib.load_library("solar_system_lib.so", "src/c")

        float64_array = np.ctypeslib.ndpointer(dtype=ctypes.c_double, ndim=1,
                                               flags="contiguous")
        lib_ss.python_interface.argstypes = [float64_array,
                                             float64_array,
                                             float64_array,
                                             float64_array,
                                             ctypes.c_int,
                                             ctypes.c_int,
                                             ctypes.c_double,
                                             ctypes.c_int,
                                             ctypes.c_int,
                                             ctypes.c_int,
                                             ctypes.c_int]

        recorded_minima = lib_ss.python_interface(
                                np.ctypeslib.as_ctypes(p),
                                np.ctypeslib.as_ctypes(v),
                                np.ctypeslib.as_ctypes(masses),
                                np.ctypeslib.as_ctypes(minima),
                                ctypes.c_int(num_bodies),
                                ctypes.c_int(steps),
                                ctypes.c_double(dt),
                                ctypes.c_int(skip_saving),
                                ctypes.c_int(perihelion_minima),
                                ctypes.c_int(integration_alg),
                                ctypes.c_int(acceleration_alg))

        post = time.clock()
        time_spent = post - pre
        if not silent:
            print "Time spent (C): %g" % time_spent
        if perihelion_minima != 0:
            minima = minima[:recorded_minima].copy()
            return p, v, minima
        return p, v

    @staticmethod
    def EnergyConservation_test():
        TestSolarSystem = SolarSystem()
        TestSolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
        TestSolarSystem.CreateCelestialObject(1, 0, 0, 2*np.pi, 3.003e-6)

        P, V = TestSolarSystem.fill_array_c(int(1e6), 15)
        t = np.linspace(0,15,int(1e6)+1)
        KineticEnergyEarth = 0.5*TestSolarSystem.ObjectMasses[1] * (V[:,1,0]**2 + V[:,1,1]**2) #SolarMasses*AU**2/yr**2
        KineticEnergySun = 0.5*TestSolarSystem.ObjectMasses[0] * (V[:,0,0]**2 + V[:,0,1]**2)
        KineticEnergy = KineticEnergySun + KineticEnergyEarth

        CenterOfMass = P[:,0,:]*TestSolarSystem.ObjectMasses[0] + P[:,1,:]*TestSolarSystem.ObjectMasses[1]
        distance = np.sqrt( (P[:,1,0] - P[:,0,0])**2 + (P[:,0,1] - P[:,1,1])**2 )
        PotentialEnergy = -G*TestSolarSystem.ObjectMasses[0]*TestSolarSystem.ObjectMasses[1]/distance

        plt.plot(t, KineticEnergy)
        plt.plot(t, PotentialEnergy)
        plt.plot(t, KineticEnergy+PotentialEnergy)
        plt.axis([0,15,-1.5e-4,1.5e-4])
        plt.title("Energy of circular Planet-Sun system over 15 years")
        plt.legend(["Kinetic Energy","Potential Energy","Total Energy"])
        plt.xlabel("time in years")
        plt.ylabel("energy in SolarMasses*AU^2/Year^2")
        plt.show()

        print "Center of mass at beginning of simulation, and after 15 years:"
        print CenterOfMass[0], "\n", CenterOfMass[-1]

        AngularMomentum = TestSolarSystem.ObjectMasses[1]*np.cross(P[:,1], V[:,1])
        plt.plot(t, AngularMomentum)
        plt.title("Angular Momentum of Planet over 15 years")
        plt.xlabel("time in years")
        plt.ylabel("Angular Momentum")
        print "Relative error in angular momentum over 15 years: %e" % (( np.min(AngularMomentum) - np.max(AngularMomentum) ) / np.min(AngularMomentum))
        plt.axis([0,15,0,4e-5])
        plt.show()

    @staticmethod
    def TimeStep_test():
        TestSolarSystem = SolarSystem()
        TestSolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
        TestSolarSystem.CreateCelestialObject(1, 0, 0, 29.8*0.210805, 3.003e-6)

        P20FE = TestSolarSystem.fill_array_c(20, 1, int_method=TestSolarSystem.ForwardEuler)[0]
        P20VV = TestSolarSystem.fill_array_c(20, 1)[0]
        P100FE = TestSolarSystem.fill_array_c(100, 1, int_method=TestSolarSystem.ForwardEuler)[0]
        P100VV = TestSolarSystem.fill_array_c(100, 1,)[0]
        plt.axes(aspect = 'equal')
        plt.plot(P20FE[:,1,0], P20FE[:,1,1], "g-")
        plt.plot(P20VV[:,1,0], P20VV[:,1,1], "r-")
        plt.plot(P100FE[:,1,0], P100VV[:,1,1], "b-")
        plt.plot(P100VV[:,1,0], P100VV[:,1,1], "k-")
        plt.plot(0,0,"yo")
        plt.axis([-2,2,-2,2])
        plt.xlabel("AU")
        plt.ylabel("AU")
        plt.title("Comparing timesteps with Velocity Verlet and Forward Euler")
        plt.legend(["dt=1/20year,FE","dt=1/20 year,VV","dt=1/100 yearFE","dt=1/100 year,VV"])
        plt.show()
