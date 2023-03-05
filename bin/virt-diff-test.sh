image=$1
name=$2

tput bold
tput setaf 2
echo "1) Access forensic image location"
tput sgr0
###mount -o username=qemu,pass=qemu,nobrl -t cifs //192.168.1.75/convertidos /mnt/destino
tput bold
tput setaf 2
echo "2) Mount forensic image"
tput sgr0
ewfmount $image /mnt/image/
tput bold
tput setaf 2
echo "3) Get image information"
tput sgr0
virt-inspector /mnt/image/ewf1 | tee /mnt/destino/soinfo-$name.txt
tput bold
tput setaf 2
echo "4) Create backing file snapshot"
tput sgr0
cd /mnt/destino
qemu-img create -f qcow2 -b /mnt/image/ewf1 -F raw snapshot-temp-$name.qcow2.snap
tput bold
tput setaf 2
echo "5) Activate nbd block device"
tput sgr0
modprobe nbd max_parts=25
qemu-nbd --connect=/dev/nbd0 snapshot-temp-$name.qcow2.snap
tput bold
tput setaf 2
echo "6) Remove hibernate file"
tput sgr0
xmllint --xpath '//mountpoint' /mnt/destino/soinfo-mobitral-drivers.txt | awk -F'"' '{print $2}' | while read line ; do
   NUMBER=$(echo $line | tr -dc '0-9')
   tput bold
   tput setaf 2
   echo "6.1) Removing hibernate file form partion number $NUMBER"
   tput sgr0
   ntfsfix /dev/nbd0p$NUMBER
   sync
   ntfsfix -d /dev/nbd0p$NUMBER
   sync
   mount -t ntfs-3g /dev/nbd0p$NUMBER /mnt/win -o remove_hiberfile
   umount /mnt/win
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
virt-v2v -i disk /mnt/destino/snapshot-temp-$name.qcow2.snap  -o qemu -of qcow2 -os /mnt/destino -on $name.qcow2
tput bold
tput setaf 2
echo "8) Umounting paths"
tput sgr0
cd ..
virt-diff -a /mnt/image/ewf1 -A /mnt/destino/snapshot-temp-$name.qcow2.snap
umount /mnt/image
##umount /mnt/destino
tput bold
tput setaf 2
echo "9) Delete temp snapshot"
tput sgr0
rm /mnt/destino/snapshot-temp-$name.qcow2.snap


