distro=$1
case $distro in
  fedora)
    suffix=fed
    ;;
  ubuntu)
    suffix=deb
    ;;
esac

if [ -z "$suffix" ]; then
  exit 1
fi

bash install_dependencies_${suffix}_minimal.sh
