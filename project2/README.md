# Project 2


## Instructions
To generate the report run
``` sh
make report
```

To (generate if necessary and) display the report run
``` sh
make show
```

Run all tests with
``` sh
make test
```

## Benchmarks
__TODO__

To setup everything for the benchmark, run
```
$ make plots
$ make clean-plots
```

Then run the following command (output included)
```
$ time make plots
for plot_prog in src/plot_b.py src/plot_d.py; do \
	python $plot_prog ; \
done
Solution for non-interacting case with omega=     1, n=200 took 1.21115 seconds
Saving plot to fig/plot_3-lowest_non-interacting_omega=1_rho-max=5_n=200.pdf
Solution for interacting case with omega=     1, n=200 took 1.21375 seconds
Saving plot to fig/plot_3-lowest_interacting_omega=1_rho-max=5_n=200.pdf
Solution for non-interacting case with omega=   0.5, n=100 took 0.084322 seconds
Solution for non-interacting case with omega=     1, n=100 took 0.085319 seconds
Solution for non-interacting case with omega=     5, n=100 took 0.091655 seconds
Saving plot to fig/plot_varying-omega_non-interacting_omega=0.5,1,5_rho-max=5_n=100.pdf
Solution for non-interacting case with omega= 0.005, n=100 took 0.075482 seconds
Solution for non-interacting case with omega=  0.01, n=100 took 0.074843 seconds
Solution for non-interacting case with omega=  0.05, n=100 took 0.071429 seconds
Saving plot to fig/plot_varying-omega_non-interacting_omega=0.005,0.01,0.05_rho-max=70_n=100.pdf
Solution for interacting case with omega=   0.5, n=100 took 0.099925 seconds
Solution for interacting case with omega=     1, n=100 took 0.085623 seconds
Solution for interacting case with omega=     5, n=100 took 0.082567 seconds
Saving plot to fig/plot_varying-omega_interacting_omega=0.5,1,5_rho-max=5_n=100.pdf
Solution for interacting case with omega= 0.005, n=100 took 0.076715 seconds
Solution for interacting case with omega=  0.01, n=100 took 0.083039 seconds
Solution for interacting case with omega=  0.05, n=100 took 0.080896 seconds
Saving plot to fig/plot_varying-omega_interacting_omega=0.005,0.01,0.05_rho-max=70_n=100.pdf

real    0m5.618s
user    0m5.812s
sys     0m2.188s
```

This was run on a i7-6560U @ 3 GHz (approximately)

## Dependencies
* Python 2 w/ SciPy stack
* texlive with most of the bells and whistles
* Compilers for C and C++
