#set -x # print all commands

function dnf_install {
    echo -e "\nAttempting to install $1 via dnf"
    sudo dnf -q -y install $1
    if [ $? -ne 0 ]; then
        echo "could not install $1 - abort"
        exit 1
    fi
}


function pip_install {
    echo -e "\nAttempting to install $1 via pip"
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

# Python tabulate for pretty tables
pip_install tabulate

# GSL
dnf_install gsl-devel

# LaTeX
dnf_install texlive-scheme-medium
dnf_install texlive-collection-bibtexextra
dnf_install texlive-collection-binextra
dnf_install texlive-collection-latexextra
dnf_install texlive-collection-publishers
dnf_install texlive-collection-science
