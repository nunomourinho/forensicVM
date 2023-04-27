#!/bin/bash

# Record the start time

start_time=$(date +%s)


# Helper function: Change qemu startup script.
function change_qemu_vm {
   vmconfig=`cat $1 | grep -v net0 | grep -v display | grep -v qxl | grep -v balloon | grep -v viosock| sed 's|/usr/share/OVMF/|/forensicVM/usr/share/qemu/|g'`
   extra_parameters="   -display vnc=0.0.0.0:0,websocket=5901 \\
       -qmp unix:$3,server,nowait \\
       -pidfile $4 \\
       -usb -device usb-tablet -device usb-kbd \\
       -vga virtio \\
       -boot menu=on,strict=on,reboot-timeout=10000,splash-time=20000,splash=/forensicVM/branding/bootsplash.jpg"

    echo "$vmconfig
    $extra_parameters" >$2
    chmod 700 $2

#       -chardev socket,id=mon0,host=localhost,port=4444,server=on,wait=off \\
#       -mon chardev=mon0,mode=control,pretty=on \\

}


# Image is the complete path for the forensic image

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "Sintaxe: forensic2v <forensic-image> <name> [copy|snap]"
    exit 1
fi

# Detect what image manager should be used to open the forensic image
imagemanager=""
if [[ -n $1 ]]; then
    qemu-img info "$1" | grep "file format" | grep qcow2
    if [[ $? -eq 0 ]]; then
        imagemanager="qemu"
    else
      ewfinfo "$1"
      if [[ $? -eq 0 ]]; then
          imagemanager="ewf"
      else
          affinfo "$1"
          if [[ $? -eq 0 ]]; then
             imagemanager="aff"
          else
              qemu-img info "$1"
              if [[ $? -eq 0 ]]; then
                 imagemanager="qemu"
              else
                 echo "Image format not detected. Aborting"
                 exit 1
              fi
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
echo $mode

image_ewf_mnt=/forensicVM/mnt/vm/$name/ewf
image_aff_mnt=/forensicVM/mnt/vm/$name/aff
win_mount=/forensicVM/mnt/vm/$name/win
run_mount=/forensicVM/mnt/vm/$name/run
qmp_socket=$run_mount/qmp.sock
run_pid=$run_mount/run.pid
vm_mount=/forensicVM/mnt/vm
tmp_mount=$vm_mount
vm_name=/forensicVM/mnt/vm/$name
info_name=/forensicVM/mnt/vm/$name/${name}.info

if [ $mode == "snap" ]; then
   touch /tmp/qemu-img-cp-now
fi

mkdir "$vm_name"
mkdir "$image_ewf_mnt"
mkdir "$image_aff_mnt"
mkdir "$win_mount"
mkdir "$run_mount"


function CleanUpINT {
     echo "CleanUp on errors"
     qemu-nbd --disconnect "/dev/nbd0"
     if [ $imagemanager == "ewf" ]; then
        umount "$image_ewf_mnt"
     fi
     if [ $imagemanager == "aff" ]; then
        umount "$image_aff_mnt"
     fi
     rm "${vm_name}/S0001-P0000.qcow2-sda"
     exit 1
}

function CleanUpEXIT {
     echo "Normal CleanUp"
     # Record the end time
     end_time=$(date +%s)


     # Calculate the elapsed time in seconds
     elapsed_time=$(($end_time - $start_time))


     # Convert the elapsed time to days, hours, minutes, and seconds
     days=$(($elapsed_time / 86400))
     hours=$(($elapsed_time / 3600 % 24))
     minutes=$(($elapsed_time / 60 % 60))
     seconds=$(($elapsed_time % 60))


     # Print the elapsed time in days, hours, minutes, and seconds
     echo "Elapsed time: $days days, $hours hours, $minutes minutes, $seconds seconds"

     exit 0
}

# Call the CleanUp function on exit

trap CleanUpINT INT
trap CleanUpEXIT EXIT


tput bold
tput setaf 2
echo "1) Access forensic image location"
tput sgr0
tput bold
tput setaf 2
echo "2) Mount forensic image"
tput sgr0

if [ $imagemanager == "ewf" ]; then
   ewfmount "$image" "$image_ewf_mnt"/
fi

if [ $imagemanager == "aff" ]; then
   affuse -o direct_io "$image" "$image_aff_mnt"/
   if [[ $? -eq 0 ]]; then
       affrawmnt="${image_aff_mnt}/`ls $image_aff_mnt`"
       echo "Image mounted on: $affrawmnt"
   else
       echo "Error: could not mount $image"
       exit 1
   fi
fi

tput bold
tput setaf 2
echo "3) Get image information"
tput sgr0
if [ $imagemanager == "ewf" ]; then
   virt-inspector "$image_ewf_mnt"/ewf1 > ${info_name}
fi

if [ $imagemanager == "aff" ]; then
   virt-inspector "$affrawmnt" > ${info_name}
fi

if [ $imagemanager == "qemu" ]; then
   virt-inspector "$1" > ${info_name}
fi


tput bold
tput setaf 2
echo "4) Create backing file snapshot"
tput sgr0
# shellcheck disable=SC2164
cd "$vm_name"
if [ $imagemanager == "ewf" ]; then
   qemu-img create -f qcow2 -b "$image_ewf_mnt"/ewf1 -F raw S0001-P0000.qcow2-sda
fi

if [ $imagemanager == "aff" ]; then
   qemu-img create -f qcow2 -b "$affrawmnt" -F raw S0001-P0000.qcow2-sda
fi

if [ $imagemanager == "qemu" ]; then
   qemu-img create -f qcow2 -b "$1" -F qcow2 S0001-P0000.qcow2-sda
fi

tput bold
tput setaf 2




echo "5) Activate nbd block device"
tput sgr0
/sbin/modprobe nbd max_parts=25
qemu-nbd --connect=/dev/nbd0 S0001-P0000.qcow2-sda
tput bold
tput setaf 2
echo "6) Remove hibernate file"
tput sgr0
# shellcheck disable=SC2162
xmllint --xpath '//mountpoint' ${info_name} | awk -F'"' '{print $2}' | while read line ; do
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
virt-v2v -i disk "$vm_name/S0001-P0000.qcow2-sda"  -o qemu -of qcow2 -os "$vm_name" -on "S0002-P0001.qcow2"
change_qemu_vm "$vm_name/S0002-P0001.qcow2.sh" "$vm_name/S0002-P0001.qcow2-vnc.sh" "$qmp_socket" "$run_pid"


if [ $mode != "snap" ]; then
  tput bold
  tput setaf 2
  echo "8) Umounting paths"
  tput sgr0
  cd ..
  if [ $imagemanager == "ewf" ]; then
     umount "$image_ewf_mnt"
  fi

  if [ $imagemanager == "aff" ]; then
     umount "$image_aff_mnt"
  fi

  tput bold
  tput setaf 2
  echo "9) Delete temp snapshot"
  tput sgr0
  rm "${vm_name}/S0001-P0000.qcow2-sda"
  echo "copy" > "${vm_name}/mode"
else
  echo "snap" > "${vm_name}/mode"
fi





