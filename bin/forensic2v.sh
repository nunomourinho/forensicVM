#!/bin/bash

# Image is the complete path for the forensic image

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "Sintaxe: forensic2v <forensic-image> <name> [copy|snap]"
    exit 1
fi

imagemanager=""
if [[ -n $1 ]]; then
    # shellcheck disable=SC1073
    # shellcheck disable=SC1072
    if [[ ewfinfo "$1" -eq 0 ]]; then
        imagemanager="ewf"
    else
        if [[ affinfo "$1" -eq 0 ]]; then
           imagemanager="aff"
        else
            if [[ qemu-img info "$1" -eq 0 ]]; then
               imagemanager="qemu"
            else
               echo "Image format not detected. Aborting"
               exit 1
            fi
        fi
    fi
else
    echo "The image parameter (1) is missing"
    exit 1
fi

echo "Converting using utility: $imagemanager"

image=$1

# Name: Name
name=$2
# shellcheck disable=SC2236
if [ ! -z "$3" ]; then
	mode=$3
else
	mode="copy"
fi

image_ewf_mnt=/forensicVM/mnt/vm/$name/ewf
win_mount=/forensicVM/mnt/vm/$name/win
vm_mount=/forensicVM/mnt/vm
tmp_mount=$vm_mount
vm_name=/forensicVM/mnt/vm/$name

if [ $mode == "snap" ]; then
   touch /tmp/qemu-img-cp-now
fi

mkdir "$vm_name"
mkdir "$image_ewf_mnt"
mkdir "$win_mount"

tput bold
tput setaf 2
echo "1) Access forensic image location"
tput sgr0
tput bold
tput setaf 2
echo "2) Mount forensic image"
tput sgr0
# run command if mode == "snap"
if [ $imagemanager == "ewf" ]; then
   ewfmount "$image" "$image_ewf_mnt"/
fi

tput bold
tput setaf 2
echo "3) Get image information"
tput sgr0
virt-inspector "$image_ewf_mnt"/ewf1 | tee $vm_mount/info-"$name".txt
tput bold
tput setaf 2
echo "4) Create backing file snapshot"
tput sgr0
# shellcheck disable=SC2164
cd "$vm_name"
qemu-img create -f qcow2 -b "$image_ewf_mnt"/ewf1 -F raw S0001-P0000-"$name".qcow2-sda
tput bold
tput setaf 2
echo "5) Activate nbd block device"
tput sgr0
/sbin/modprobe nbd max_parts=25
qemu-nbd --connect=/dev/nbd0 S0001-P0000-"$name".qcow2-sda
tput bold
tput setaf 2
echo "6) Remove hibernate file"
tput sgr0
# shellcheck disable=SC2162
xmllint --xpath '//mountpoint' $vm_mount/info-"$name".txt | awk -F'"' '{print $2}' | while read line ; do
   NUMBER=$(echo "$line" | tr -dc '0-9')
   tput bold
   tput setaf 2
   echo "6.1) Removing hibernate file form partition number $NUMBER"
   tput sgr0
   ntfsfix "/dev/nbd0p$NUMBER"
   sync
   ntfsfix -d "/dev/nbd0p$NUMBER"
   sync
   mount -t ntfs-3g "/dev/nbd0p$NUMBER" "$win_mount" -o remove_hiberfile
   umount  "$win_mount"
   ntfsfix "/dev/nbd0p$NUMBER"
   sync
   ntfsfix -d "/dev/nbd0p$NUMBER"
done
qemu-nbd --disconnect "/dev/nbd0"
sync
tput bold
tput setaf 2
echo "7) Add virtio drivers and qemu guest"
tput sgr0
virt-v2v -i disk "$vm_name/S0001-P0000-$name.qcow2-sda"  -o qemu -of qcow2 -os "$vm_name" -on "S0002-P0001-$name.qcow2"
if [ $mode != "snap" ]; then
  tput bold
  tput setaf 2
  echo "8) Umounting paths"
  tput sgr0
  cd ..
  umount  "$image_ewf_mnt"
  tput bold
  tput setaf 2
  echo "9) Delete temp snapshot"
  tput sgr0
  rm "$tmp_mount/snapshot-temp-$name.qcow2.snap"
fi
