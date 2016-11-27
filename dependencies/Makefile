.PHONY: all Ubuntu Debian RedHat Fedora
OS=$(shell lsb_release -si)

debian_script=install_dependencies_deb.sh
fedora_script=install_dependencies_fed.sh

all: $(OS)

Ubuntu: Debian
Debian: $(debian_script)
	bash $(debian_script)
RedHat: Fedora
Fedora: $(fedora_script)
	bash $(fedora_script)
