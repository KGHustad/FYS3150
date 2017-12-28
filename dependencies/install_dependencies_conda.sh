env_prefix=$(python -c "import os, sys; conda_bin=os.path.dirname(sys.executable); print (os.path.normpath(os.path.join(conda_bin, '..')))")
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

conda install -y numpy scipy matplotlib pytest gsl openmp

# copy in scripts that update environment variables to ensure that libraries installed in the environment (really just GSL in this case) are detected
mkdir -p $env_prefix/etc/conda/activate.d && cp $DIR/conda_activate.sh $env_prefix/etc/conda/activate.d/lib.sh
mkdir -p $env_prefix/etc/conda/deactivate.d && cp $DIR/conda_deactivate.sh $env_prefix/etc/conda/deactivate.d/lib.sh
