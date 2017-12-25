#/usr/bin/env sh
apt-get update
apt-get install locales -y
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
apt-get install python-pip -y

apt-get install python-numpy -y
apt-get install python-scipy -y
apt-get install python-matplotlib -y
apt-get install python-nose -y

pip install -U pytest

# tabulate is used for pretty printing tables
pip install tabulate

# Valgrind for memory checks
apt-get install valgrind -y

# The GNU Scientific Library is used for RNGs
apt-get install libgsl-dev -y

# GSL should be linked to atlas for decent linear algebra performance (probably irrelevant for our use)
apt-get install libatlas-base-dev -y


# MPI
# OpenMPI
apt-get install openmpi-bin libopenmpi-dev -y

# mpi4py for using MPI from Python
pip install mpi4py
