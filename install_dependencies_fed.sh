set -x # print all commands

function dnf_install {
    sudo dnf -y install $1
    if [ $? -ne 0 ]; then
        echo "could not install $1 - abort"
        exit 1
    fi
}


function pip_install {
    sudo -H pip install --upgrade "$@"
    if [ $? -ne 0 ]; then
        echo "could not install $p - abort"
        exit 1
    fi
}


# Python 2 w/ SciPy stack (unused parts commented out)
dnf_install python
dnf_install numpy
dnf_install scipy
dnf_install python-matplotlib
#dnf_install ipython
#dnf_install python-pandas
#dnf_install sympy
dnf_install python-nose
dnf_install atlas-devel


# Compilers for C and C++ and language extensions
dnf_install gcc
dnf_install gcc-c++
dnf_install libgomp
dnf_install openmpi-devel

# MPI for Python
dnf_install mpi4py-common

# GSL
dnf_install gsl-devel
