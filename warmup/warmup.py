import numpy as np
import matplotlib.pyplot as plt

x = np.sqrt(2)

exact=1./3

def f(x):
	return np.arctan(x)

def f2c(x,h):
	return (f(x+h)-f(x))/h

def f3c(x,h):
	return (f(x+h)-f(x-h))/(2*h)

h_ = np.linspace(0,150)

j = lambda x: 10**(-2-0.1*x)
	
h = j(h_)

f2ccomputed = np.zeros(150)
f3ccomputed = np.zeros(150)

f2ccomputed = f2c(x,h)
f3ccomputed = f3c(x,h)
f2cerror = abs(f2ccomputed - exact)
f3cerror = abs(f3ccomputed - exact)

def write2file(filename, f2cerror, f3cerror, exact):
	outfile = open(filename,"w")
	outfile.write("%10s %10s %10s\n" % ("h","f2c error", "f3c error"))
	for i in range(len(h_)):
		outfile.write("%10.2e %10.2e %10.2e \n" %(h[i],f2cerror[i],f3cerror[i]))
	outfile.close()

write2file("data.txt", f2cerror, f3cerror, exact)

def log_10(f_comp, f_exact):
	return np.log10(abs((f_comp-f_exact)/(f_exact)))

plt.plot(np.log10(h), log_10(f2ccomputed, exact))
plt.plot(np.log10(h), log_10(f3ccomputed, exact))
plt.xlabel("h")
plt.ylabel("relative error")
plt.show()
