import numpy as np
import matplotlib.pyplot as plt

def u_func(x):
	return 1-(1-np.exp(-10))*x-np.exp(-10*x)

def f_func(x):
	return 100*np.exp(-10*x)

def solve_specific(f_func, n):
	x = np.linspace(0, 1, n+2)
	h = x[1] - x[0]
	f = f_func(x)*h**2
	u = np.zeros(n+2)
	a_func = lambda i: (i+1)/i
	a = a_func(np.arange(0,n+1, dtype=np.float64))
	a[0] = 0 #fysiker loesning
	for i in range(2,n+1):
		f[i] = f[i] + f[i-1]/a[i-1]	# 2 FLOPS
	
	u[n] = f[n]/float(a[n])

	for i in range(n-1,0,-1):
		u[i] = (f[i]+u[i+1])/a[i]	# 2 FLOPS

	return u, x

def plot_func(f_func, n):
	u, x = solve_specific(f_func, n)
	plt.plot(x, u, x, u_func(x))

for n in ([10,100,1000]):
	a = np.full(n+2, 2, dtype=np.float64)
	b = np.full(n+2, -1, dtype=np.float64)
	c = np.full(n+2, -1, dtype=np.float64)
	plot_func(f_func, n)
plt.show()

def CPU_time(n):
	import time
	from task_b import solve_general

	a = np.full(n+2, 2, dtype=np.float64)
	b = np.full(n+2, -1, dtype=np.float64)
	c = np.full(n+2, -1, dtype=np.float64)

	start_time = time.time()
	u,x = solve_general(f_func, n, a, b, c)
	print "General function run-time: %f seconds" % (time.time() - start_time)
	
	start_time = time.time()
	u,x = solve_specific(f_func, n)
	print "Specific function run-time: %f seconds" % (time.time() - start_time)

CPU_time(10**6)
