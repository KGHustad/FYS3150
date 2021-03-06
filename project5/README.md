# Project 5 - Partial Differential Equations


## Pre/post-deadline versions
A few minor bugs have been corrected after the deadline. To get the last version before the deadline, run
``` sh
git checkout project5-delivery
```

To return to the latest commit, run
``` sh
git checkout master
```

## Instructions
To generate the report run
``` sh
make report
```

To (generate if necessary and) display the report run
``` sh
make show
```

To make the C library run
``` sh
make diffusion_lib
```

## Unit tests
The test suite can be run with
``` sh
make test
```


## Reference test
See the unit tests.

## Dependencies
* Python 2 w/ SciPy stack
* texlive with most of the bells and whistles
* Compilers for C and C with MPI (`cc` and `mpicc`)
* Valgrind
* mpi4py (can be installed via pip)
