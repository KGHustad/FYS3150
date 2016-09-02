import numpy as np
import matplotlib.pyplot as plt

def u_func(x):
	return 1-(1-np.exp(-10))*x-np.exp(-10*x)

def f_func(x):
	return 100*np.exp(-10*x)

def solve_general(f_func, n, a, b, c):
	x = np.linspace(0, 1, n+2)
	h = x[1] - x[0]
	f = f_func(x)*h**2
	u = np.zeros(n+2)

	for i in range(2,n+1): #Forward Substitution
		a[i] = a[i] - (b[i-1]*c[i])/a[i-1]        # 3 FLOPS
		f[i] = f[i] - f[i-1]*c[i]/a[i-1]   # 3 FLOPS

	#Backward Substitution
	u[n] = f[n]/float(a[n])

	for i in range(n-1,0,-1):
		u[i] = (f[i] - b[i]*u[i+1]) / a[i]          # 3 FLOPS

	return u, x

def plot_func(f_func, n, a, b, c):
	u, x = solve_general(f_func, n, a, b, c)
	plt.plot(x, u, x, u_func(x))

for n in ([10,100,1000]):
	a = np.full(n+2, 2, dtype=np.float64)
	b = np.full(n+2, -1, dtype=np.float64)
	c = np.full(n+2, -1, dtype=np.float64)
	plot_func(f_func, n, a, b, c)
plt.show()
