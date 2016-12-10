import sys
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
from operator import itemgetter
from task_e import *

filenames = sys.argv[1:]

if len(sys.argv) < 2:
    print "USAGE: python %s <data file>" % (sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]
with open(filename, 'r') as f:
    data_dict = pickle.load(f)
L_values = data_dict['L_values']
T_values = data_dict['T_values']
length = len(T_values)
specific_heat = np.zeros(length)

critical_temps_abs = []
critical_temps_fit = []

for L in L_values:
    print "L = %d" % L
    specific_heat = [data_dict[(L, T)]['specific_heat'] for T in T_values]
    specific_heat = np.array(specific_heat)/L**2

    abs_max_i = specific_heat.argmax()
    print "Absolute max              @ T=%.5f    Specific heat: %.5f" % (T_values[abs_max_i], specific_heat[abs_max_i])
    critical_temps_abs.append(T_values[abs_max_i])

    near = 10
    T_peak = T_values[abs_max_i-near: abs_max_i+near]

    p = np.polyfit(T_peak, specific_heat[abs_max_i-near: abs_max_i+near], 2)
    def eval_poly(p, x):
        s = 0
        for degree, coeff in enumerate(reversed(p)):
            if degree == 0:
                s = coeff
            else:
                s += coeff*x**degree
        return s

    def poly_max(p):
        import sympy
        x = sympy.symbols('x')
        full_poly = eval_poly(p, x)
        diff_poly = sympy.diff(full_poly, x)
        zeros = sympy.solveset(diff_poly, x)
        candidates = [(zero, full_poly.subs(x, zero)) for zero in zeros]
        return max(candidates, key=itemgetter(1))

    pol_max_T, pol_max_heat = poly_max(p)
    print "Second order poly fit max @ T=%.5f    Specific heat: %.5f" % (pol_max_T, pol_max_heat)

    critical_temps_fit.append(pol_max_T)

    fit_specific_heat = eval_poly(p, T_values)
    plt.plot(T_values, fit_specific_heat, label='L = %d (fit)' % L)
    plt.plot(T_values, specific_heat, label='L = %d (data)' % L)

    print

def approx_critical_temp(approx, L):
    T_c_b = approx[-2]
    T_c_a = approx[-1]
    L_b = L[-2]
    L_a = L[-1]

    a = (T_c_b - T_c_a) / (1./L_b - 1./L_a)
    T_c_approx = T_c_a - a/L_a
    return T_c_approx

T_c_exact = 2 / (np.log(1 + np.sqrt(2)))
T_c_abs = approx_critical_temp(critical_temps_abs, L_values)
T_c_fit = approx_critical_temp(critical_temps_fit, L_values)

print "T_c with abs: %8g    Error: %8g" % (T_c_abs, (T_c_abs - T_c_exact))
print "T_c with fit: %8g    Error: %8g" % (T_c_fit, (T_c_fit - T_c_exact))

plt.legend(loc='best')
plt.show()
