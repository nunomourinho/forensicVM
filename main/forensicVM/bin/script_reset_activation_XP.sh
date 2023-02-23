rand_name=`cat /dev/urandom | tr -cd 'a-f0-9' | head -c 7;`
cp /forensicVM/scripts/reset_ActivationXP.bat /tmp/reset_ActivationXP$rand_name.bat
virt-customize -a $1 -firstboot /tmp/reset_ActivationXP$rand_name.bat
rm /tmp/reset_ActivationXP$rand_name.bat
