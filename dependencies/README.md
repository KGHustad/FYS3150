This directory contains bash scripts which install dependencies for distros based on Debian or Fedora.

### Automatic distro detecting
There are two ways to automagically run the correct install script:

A Python script (this is probably the most robust option), which can be run with

``` sh
python install_dependencies.py
```

A GNU Makefile, which can be run with
``` sh
make
```
