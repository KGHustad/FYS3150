#/usr/bin/env python
import subprocess
import sys

def determine_OS():
    OS = subprocess.check_output(["uname"]).strip()
    return OS


def determine_distro():
    distro = subprocess.check_output(["lsb_release", "-si"]).strip()
    return distro

install_scripts = {'debian': 'install_dependencies_deb.sh',
'fedora': 'install_dependencies_fed.sh'}

def determine_target():
    OS = determine_OS()
    if "linux" in OS.lower():
        distro = determine_distro()
        return distro
    print "ERROR: Your OS is not supported by this install script."
    sys.exit(1)

def handle_target(target):
    install_script = None
    if target in ['Debian', 'Ubuntu']:
        # debian based
        install_script = install_scripts['debian']
    elif target == 'Fedora' or target.startswith('RedHat'):
        # fedora based
        install_script = install_scripts['fedora']
    subprocess.call(['bash', install_script])

if __name__ == '__main__':
    target = determine_target()
    handle_target(target)
    #script = install_scripts[target]
