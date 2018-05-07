#/usr/bin/env bash
# tabulate is used for pretty printing tables
sudo -H pip install tabulate

# Valgrind for memory checks
sudo apt-get install valgrind -y

# The GNU Scientific Library is used for RNGs
sudo apt-get install libgsl-dev -y

# GSL should be linked to atlas for decent linear algebra performance (probably irrelevant for our use)
sudo apt-get install libatlas-base-dev -y


# MPI
# OpenMPI
sudo apt-get install openmpi-bin openmpi-doc libopenmpi-dev -y

# mpi4py for using MPI from Python
sudo -H pip install mpi4py
