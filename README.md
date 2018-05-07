# FYS3150 - Computational physics
Travis [![Travis CI Build Status](https://travis-ci.org/KGHustad/FYS3150.svg?branch=master)](https://travis-ci.org/KGHustad/FYS3150) Drone [![Drone CI Build Status](https://drone.doconce.org/api/badges/KGHustad/FYS3150/status.svg)](https://drone.doconce.org/api/badges/KGHustad/FYS3150/status.svg)

This repository contains the coursework of Kristian Gregorius Hustad and Jonas Gahr Sturtzel Lunde from the autumn of 2016.

## Note on compatibility
The programs in this repository were originally developed for Ubuntu 16.04 with Python 2.7. Support for Fedora and OS X has since been added.

## Dependencies
To install (hopefully) all dependencies, run
``` sh
make dependencies
```

On Mac, `conda` is needed to install dependencies. With conda installed, it is recommended create a separate environment (called `fys3150` in the example below), before running the install script.
``` sh
conda create -n fys3150 python=2.7
source activate fys3150
bash dependencies/install_dependencies_conda.sh
# deactivate and reactivate to get GSL added to the library path
source deactivate
source activate fys3150
```

This environment can later be removed with
``` sh
conda env remove --name fys3150
```

Refer to [the conda docs](https://conda.io/docs/user-guide/tasks/manage-environments.html) for more information on managing conda enviroments.

## Make all projects
To make all projects, run
``` sh
make
```

This may take a few minutes.

## Travis
We have set up [Travis CI](https://travis-ci.org/KGHustad/FYS3150) with this repository to compile our C libraries and run tests automatically at every push.
