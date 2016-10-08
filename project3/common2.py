import numpy as np
import matplotlib.pyplot as plt

years = 1
steps_per_year = 10
steps = int(years*steps_per_year)
dt = 1.0/steps_per_year
G = 4*np.pi**2
planets = 1

p = np.zeros(shape=(steps,2,planets))
v = np.zeros(shape=(steps,2,planets))

p[0,0,0] = 1
p[0,1,0] = 0

time_array = np.linspace(0,years,steps)

def acc(p):
    x,y = p
    return np.array(((-G*M*x)/((x**2+y**2)**(3./2)), (-G*M*y)/((x**2+y**2)**(3./2))))

def Fill_Array():
    #Run an integration loop for a desired amound of years, and fill the positions into an array.
    for i in xrange(steps-1):
        p[i+1] = p[i] + v[i]*dt + 0.5*acc(p[i])*dt**2
        v[i+1] = v[i] + 0.5*(acc(p[i])+acc(p[i+1]))*dt

Fill_Array
print p,v

plt.plot(p[:,0,0], p[:,1,0], "ro")
plt.show()
