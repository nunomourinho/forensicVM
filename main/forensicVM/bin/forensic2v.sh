# Image is the complete path for the forensic image or directory (in case aff directory)
image=$1

# Name: Name
name=$2
if [ ! -z "$3"]; then
	mode=$3
else
	mode="copy"
fi

image_ewf_mnt=/forensicVM/mnt/vm/$name/ewf
win_mount=/forensicVM/mnt/win
vm_mount=/forensicVM/mnt/vm
tmp_mount=$vm_mount
vm_name=/forensicVM/mnt/vm/$name

if [ mode == "snap]; then
   touch /tmp/qemu-img-cp-now
fi

mkdir $vm_name
mkdir $image_ewf_mnt
tput bold
tput setaf 2
echo "1) Access forensic image location"
tput sgr0
###mount -o username=qemu,pass=qemu,nobrl -t cifs //192.168.1.75/convertidos /mnt/destino
tput bold
tput setaf 2
echo "2) Mount forensic image"
tput sgr0
ewfmount "$image" $image_ewf_mnt/
tput bold
tput setaf 2
echo "3) Get image information"
tput sgr0
virt-inspector $image_ewf_mnt/ewf1 | tee $vm_mount/info-$name.txt
tput bold
tput setaf 2
echo "4) Create backing file snapshot"
tput sgr0
cd $vm_name
qemu-img create -f qcow2 -b $image_ewf_mnt/ewf1 -F raw S0001-P0000-$name.qcow2-sda
tput bold
tput setaf 2
echo "5) Activate nbd block device"
tput sgr0
/sbin/modprobe nbd max_parts=25
qemu-nbd --connect=/dev/nbd0 S0001-P0000-$name.qcow2-sda
tput bold
tput setaf 2
echo "6) Remove hibernate file"
tput sgr0
xmllint --xpath '//mountpoint' $vm_mount/info-$name.txt | awk -F'"' '{print $2}' | while read line ; do
   NUMBER=$(echo $line | tr -dc '0-9')
   tput bold
   tput setaf 2
   echo "6.1) Removing hibernate file form partion number $NUMBER"
   tput sgr0
   ntfsfix /dev/nbd0p$NUMBER
   sync
   ntfsfix -d /dev/nbd0p$NUMBER
   sync
   mount -t ntfs-3g /dev/nbd0p$NUMBER $win_mount -o remove_hiberfile
   umount  $win_mount
   ntfsfix /dev/nbd0p$NUMBER
   sync
   ntfsfix -d /dev/nbd0p$NUMBER
done
qemu-nbd --disconnect /dev/nbd0
sync
tput bold
tput setaf 2
echo "7) Add virtio drivers and qemu guest"
tput sgr0
virt-v2v -i disk $vm_name/S0001-P0000-$name.qcow2-sda  -o qemu -of qcow2 -os $vm_name -on S0002-P0001-$name.qcow2
if [ mode != "snap]; then
  tput bold
  tput setaf 2
  echo "8) Umounting paths"
  tput sgr0
  cd ..
  umount  $image_ewf_mnt
  tput bold
  tput setaf 2
  echo "9) Delete temp snapshot"
  tput sgr0
  rm $tmp_mount/snapshot-temp-$name.qcow2.snap
fi
