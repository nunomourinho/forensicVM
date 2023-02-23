rand_name=`cat /dev/urandom | tr -cd 'a-f0-9' | head -c 7;`
cp /forensicVM/scripts/add_forensicAdmin.bat /tmp/add_forensicAdmin$rand_name.bat
virt-customize -a $1 -firstboot /tmp/add_forensicAdmin$rand_name.bat
rm /tmp/add_forensicAdmin$rand_name.bat
