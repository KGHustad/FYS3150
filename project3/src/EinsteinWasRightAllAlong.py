from common import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import math
import argparse
import os

def find_perihelion(pos_star, pos_celbody):
    dist = np.linalg.norm(pos_star - pos_celbody, axis=1)
    local_minima_indices = scipy.signal.argrelmin(dist)
    pos_minima = pos_celbody[local_minima_indices]
    angles = np.arctan(pos_minima[:,1] /  pos_minima[:,0])
    return pos_minima, angles, local_minima_indices

def find_perihelion_alt(minima):
    """ minima elements are on the form
    [pos_x, pos_y, vel_x, vel_y, dist, time]
    """
    pos_minima = minima[:,:2]
    time_minima = minima[:,5]
    angles = np.arctan(pos_minima[:,1] /  pos_minima[:,0])
    return pos_minima, angles, time_minima


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-N', '-n',
                    dest='N', metavar='N', type=float, default=int(1E6),
                    help="total time steps stored")
parser.add_argument('-y', '--years',
                    dest='years', metavar='years', type=float, default=100,
                    help="duration of simulation in Earth years")
parser.add_argument('-s', '--skip_saving',
                    dest='skip_saving', metavar='skip_saving',
                    type=int, default=100,
                    help="time steps computed for each stored")
parser.add_argument('-p', '--perihelion_minima',
                    dest='perihelion_minima', metavar='perihelion_minima',
                    type=int, default=1000,
                    help="max number of minima to store")
parser.add_argument('--show',
                    action='store_true', default=False,
                    help='show plot')

args = parser.parse_args()
N = int(args.N)
years = args.years
skip_saving=args.skip_saving
perihelion_minima = args.perihelion_minima
# set to a number larger than expected minima
show = args.show


#time_steps = np.linspace(0, years, N+1)
dt = years/float(N*skip_saving)
print("dt = %g" % dt)
radians_to_arcseconds = 360*60*60 /(2*math.pi)

mercurymass = 0.1652e-6
mercuryspeed = 12.44
mercury_perihelion_distance = 0.3075

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
MySolarSystem.CreateCelestialObject(mercury_perihelion_distance, 0, 0, mercuryspeed, mercurymass,
#adjust_sun=True
)

# newton
p_newton, v_newton, minima_newton = MySolarSystem.fill_array_c(N, years, skip_saving=skip_saving, perihelion_minima=perihelion_minima)
v_newton = None     # allow for garbage collection
"""
res_newton = find_perihelion(p_newton[:,0,:], p_newton[:,1,:])
points_newton, angles_newton, indices_newton = res_newton
"""
points_newton, angles_newton, times_newton = find_perihelion_alt(minima_newton)


# einstein
p_einstein, v_einstein, minima_einstein = MySolarSystem.fill_array_c(N, years, acc_method=MySolarSystem.AccRelativistic, skip_saving=skip_saving, perihelion_minima=perihelion_minima)
v_einstein = None   # allow for garbage collection
"""
res_einstein = find_perihelion(p_einstein[:,0,:], p_einstein[:,1,:])
points_einstein, angles_einstein, indices_einstein = res_einstein
"""
points_einstein, angles_einstein, times_einstein = find_perihelion_alt(minima_einstein)

"""
#print(indices_newton)
#print(time_steps[indices_einstein])
#print(angles_newton)
plt.plot(time_steps[indices_newton], angles_newton, 'o-')
plt.plot(time_steps[indices_einstein], angles_einstein, 'o-')
"""
plt.plot(times_newton, angles_newton*radians_to_arcseconds, '-')
plt.plot(times_einstein, angles_einstein*radians_to_arcseconds, '-')


plt.title("Change in perihelion angle over a century\n$\Delta t$ = %g" % dt)
plt.legend(["Classical Mechanics case", "Relativistic case"], loc="best")
plt.xlabel("time in years")
plt.ylabel("angle in seconds of arc")
plt.tight_layout()
plt.savefig(os.path.join(get_fig_dir(),
            "perihelion_%03dyears_dt=%g.pdf" % (years, dt)))
if show:
    plt.show()
plt.clf()

plt.axes(aspect='equal')
plt.plot(0,0, "yo")
plt.plot(p_newton[::100,1,0], p_newton[::100,1,1], "r-")
plt.plot(p_einstein[::100,1,0], p_einstein[::100,1,1], "b-")
plt.plot(p_newton[-1,1,0], p_newton[-1,1,1], "ro")
plt.plot(p_einstein[-1,1,0], p_einstein[-1,1,1], "bo")
plt.plot(points_einstein[:,0], points_einstein[:,1], "ko")
if show:
    plt.show()
#"""

try:
    precession_newton = angles_newton[-1]*100/times_newton[-1]
    precession_newton *= radians_to_arcseconds
    precession_einstein = angles_einstein[-1]*100/times_einstein[-1]
    precession_einstein *= radians_to_arcseconds
    print("Precession per 100 years (Newton):   %g" % (precession_newton))
    print("Precession per 100 years (Einstein): %g" % (precession_einstein))
    print("Observed perihelions (Newton):   %d" % len(points_newton))
    print("Observed perihelions (Einstein): %d" % len(points_einstein))
except IndexError:
    print("*** ERROR: No minima (perihelions) found")
    print("Isaac")
    print(p_newton[:10,:,:])
    print("Albert")
    print(p_einstein[:10,:,:])
