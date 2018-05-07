env_prefix=$(python -c "import os, sys; conda_bin=os.path.dirname(sys.executable); print (os.path.normpath(os.path.join(conda_bin, '..')))")

# Restore old environment variables
export C_INCLUDE_PATH=$OLD_C_INCLUDE_PATH
export DYLD_FALLBACK_LIBRARY_PATH=$OLD_DYLD_FALLBACK_LIBRARY_PATH
export LIBRARY_PATH=$OLD_LIBRARY_PATH
unset OLD_C_INCLUDE_PATH
unset OLD_DYLD_FALLBACK_LIBRARY_PATH
unset OLD_LIBRARY_PATH
