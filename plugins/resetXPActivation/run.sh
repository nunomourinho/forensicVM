PLUGIN_NAME=""
PLUGIN_DESCRIPTION=""
OS_NAME="windows"
OS_VERSION=("xp")
AUTHOR="Nuno Mourinho"
VERSION="1.0"
LICENSE="GPL"

/forensicVM/bin/remove-hibernation.sh $1
rand_name=`cat /dev/urandom | tr -cd 'a-f0-9' | head -c 7;`
cp /forensicVM/plugins/resetXPActivation/resetXP.bat /tmp/resetXPActivation$rand_name.bat
virt-customize -a $1 -firstboot /tmp/resetXPActivation$rand_name.bat
rm /tmp/resetXPActivation$rand_name.bat


