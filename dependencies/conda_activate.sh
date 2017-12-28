env_prefix=$(python -c "import os, sys; conda_bin=os.path.dirname(sys.executable); print (os.path.normpath(os.path.join(conda_bin, '..')))")

# Store old environment variables
export OLD_C_INCLUDE_PATH=$C_INCLUDE_PATH
export OLD_DYLD_FALLBACK_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH
export OLD_LIBRARY_PATH=$LIBRARY_PATH

# Set new environment variables
export C_INCLUDE_PATH=${env_prefix}/include:$C_INCLUDE_PATH
export DYLD_FALLBACK_LIBRARY_PATH=${env_prefix}/lib:$DYLD_FALLBACK_LIBRARY_PATH
export LIBRARY_PATH=${env_prefix}/lib:$LIBRARY_PATH