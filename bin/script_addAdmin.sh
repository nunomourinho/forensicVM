PLUGIN_NAME=""
PLUGIN_DESCRIPTION=""
OS_NAME="windows"
OS_VERSION=("xp" "7" "8" "8.1" "10" "11")
AUTHOR="Nuno Mourinho"
VERSION="1.0"
LICENSE="GPL"

/forensicVM/bin/remove-hibernation.sh $1
rand_name=`cat /dev/urandom | tr -cd 'a-f0-9' | head -c 7;`
cp /forensicVM/scripts/add_forensicAdmin.bat /tmp/add_forensicAdmin$rand_name.bat
virt-customize -a $1 -firstboot /tmp/add_forensicAdmin$rand_name.bat
rm /tmp/add_forensicAdmin$rand_name.bat


