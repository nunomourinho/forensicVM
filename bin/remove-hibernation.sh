if [ -z "$1" ]; then
    echo "sintaxe: disable-hibernation.sh <image.qcow2>"
    exit 1
fi

image=$1
randname=`cat /dev/urandom | tr -cd 'a-f0-9' | head -c 7;`
tput sgr0
win_mount="/tmp/$randname-win"
mkdir ${win_mount}
tput bold
tput setaf 2
echo "Inspect image $1"
tput sgr0
virt-inspector $image > /tmp/$randname.txt
/sbin/modprobe nbd max_parts=25
first_nbd=""
for nbd_device in /dev/nbd*; do
    /sbin/nbd-client -c $nbd_device
    if [[ $? -eq 1 ]]; then
        first_nbd=$nbd_device
        echo $first_nbd
        break
    fi
done

if [ -n "$first_nbd" ]; then
    echo "First available NBD device: $first_nbd"
else
    echo "First available NBD device: $first_nbd"
    echo "Error: No available NBD devices found"
    exit 1
fi
qemu-nbd --connect=$first_nbd $image
tput bold
tput setaf 2
echo "Remove hibernate file"
tput sgr0
xmllint --xpath '//mountpoint' /tmp/$randname.txt | awk -F'"' '{print $2}' | while read line ; do
   NUMBER=$(echo $line | tr -dc '0-9')
   tput bold
   tput setaf 2
   echo "Removing hibernate file form partion number $NUMBER"
   tput sgr0
   ntfsfix ${first_nbd}p${NUMBER}
   sync
   ntfsfix -d ${first_nbd}p${NUMBER}
   sync
   mount -t ntfs-3g ${first_nbd}p${NUMBER} $win_mount -o remove_hiberfile
   umount  $win_mount
   ntfsfix ${first_nbd}p${NUMBER}
   sync
   ntfsfix -d ${first_nbd}p${NUMBER}
done
qemu-nbd --disconnect $first_nbd
sync
tput sgr0
rmdir ${win_mount}

