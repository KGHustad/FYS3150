#/usr/bin/env bash

function apt_install {
    echo -e "\nAttempting to install $1 via dnf"
    apt-get -q -y install $@
    if [ $? -ne 0 ]; then
        echo "could not install $1 - abort"
        exit 1
    fi
}

function pip_install {
    echo -e "\nAttempting to install $1 via pip"
    pip install --upgrade "$@"
    if [ $? -ne 0 ]; then
        echo "could not install $p - abort"
        exit 1
    fi
}

apt-get update

apt_install lsb-release

apt_install python-pip

apt_install python-numpy
apt_install python-scipy
apt_install python-matplotlib
apt_install python-nose

pip_install pytest

# tabulate is used for pretty printing tables
pip_install tabulate

# Valgrind for memory checks
apt_install valgrind

# The GNU Scientific Library is used for RNGs
apt_install libgsl-dev

# GSL should be linked to atlas for decent linear algebra performance (probably irrelevant for our use)
apt_install libatlas-base-dev


# MPI
# OpenMPI
apt_install openmpi-bin libopenmpi-dev

# mpi4py for using MPI from Python
pip_install mpi4py
