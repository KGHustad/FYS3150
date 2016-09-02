import matplotlib.pyplot as plt
import numpy as np

def u(x):
	return 1-(1-np.exp(-10))*x-np.exp(-10*x)

def solve(f_func, n, a, b, c):
	x = np.linspace(0, 1, n)
	h = x[1] - x[0]
	f = f_func(x)*h**2
	u = np.zeros(n)

	a_marked = np.zeros(n)
	a_marked[0] = a[0]

	b_marked = np.zeros(n)
	b_marked[0] = b[0]

	f_marked = np.zeros(n)

	for i in range(1,n): #Forward Substitution
		a_marked[i] = a[i] - (b[i-1]*c[i-1])/a_marked[i-1]
		f_marked[i] = f[i] - f_marked[i-1]*c[i-1]/float(a_marked[i-1])

	#Backward Substitution
	u[n-2] = f_marked[n-1]/float(a_marked[n-1])

	for i in range(n-3,0,-1):
		u[i] = (f_marked[i] - b[i]*u[i+1]) / a_marked[i]

	return u, x

n = 100000

a = np.full(n, 2)
b = np.full(n-1, -1)
c = np.full(n-1, -1)

f_func = lambda x: 100*np.exp(-10*x)

u_10, x_10 = solve(f_func, 10, a, b, c)
u_100, x_100 = solve(f_func, 100, a, b, c)
u_1000, x_1000 = solve(f_func, 1000, a, b, c)



plt.plot(x_10, u_10, x_100, u_100, x_1000, u_1000, x_1000, u(x_1000))
plt.show()
