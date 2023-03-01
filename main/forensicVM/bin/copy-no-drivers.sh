
image=$1
name=$2

#echo "1) Access forensic image location"
#mount -o username=qemu,pass=qemu,nobrl -t cifs //192.168.1.75/convertidos /mnt/destino

echo "1) Mount forensic image"
ewfmount $image /mnt/image/
echo "2) Convert forensic image to qcow2 format - with no drivers or guest agent"
qemu-img convert -p -f raw -O qcow2 /mnt/image/ewf1 /mnt/destino/$name.qcow2
echo "3) Umount folders"
umount /mnt/image

#umount /mnt/destino
