# Project 4

The code was developed by Kristian Gregorius Hustad and Jonas Gahr Sturtzel Lunde.

The reports are individual.

## Pre/post-deadline versions
Some minor changes have been made after the deadline. To get the last version before the deadline, run
``` sh
git checkout project4-delivery
```

## Instructions
To make the C library run
``` sh
make libising
```

To generate KGH's report run
``` sh
make report_kgh
```




## Reference test
See `reference_test.md`

## Dependencies
* A \*NIX system (`/dev/urandom` is used to seed RNGs)
* A C compiler (testing was done with GCC)
* Python 2 w/ SciPy stack
* The Python package `tabulate` [can be installed with pip](https://pypi.python.org/pypi/tabulate)
* The GNU Scientific Library (GSL)
* The Automatically Tuned Linear Algebra Software library (ATLAS)
* texlive with most of the bells and whistles
