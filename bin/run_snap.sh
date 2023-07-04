#!/bin/bash

# Image is the complete path for the forensic image

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "Sintaxe: run-snap <forensic-image> <name>"
    read -p "Image not detected"
    exit 1
fi

# Record the start time
start_time=$(date +%s)
first_nbd=$(get_first_free_nbd)
first_nbd="/dev/nbd2"
echo $first_nbd


check_disk_partitions() {
  local image_file="$1"

  # Use fdisk to check disk partitions and grep for "not in disk order"
  if fdisk -lu "$image_file" | grep -q "not in disk order"; then
    echo "Invalid partitions detected in $image_file"
    return 1
  else
    echo "No invalid partitions found in $image_file"
    return 0
  fi
}

get_first_free_nbd() {
    for nbd_device in /dev/nbd*; do
        echo $nbd_device
        if ! $(lsblk -l | grep -q "^${nbd_device#/dev/}"); then
            echo "$nbd_device"
            return
        fi
    done
    echo ""
}



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
                 read -p "Image not detected"
                 exit 1
              fi
          fi
      fi
  fi
  else
      echo "The image parameter (1) is missing"
      read -p "Image not detected"
      exit 1
fi

echo "Converting using utility: $imagemanager"

image=$1
name=$2
mode="snap"

image_ewf_mnt=/forensicVM/mnt/vm/$name/ewf
image_aff_mnt=/forensicVM/mnt/vm/$name/aff
win_mount=/forensicVM/mnt/vm/$name/win
run_mount=/forensicVM/mnt/vm/$name/run
evidence_disk=/forensicVM/mnt/vm/$name/evidence.qcow2

vm_mount=/forensicVM/mnt/vm
tmp_mount=$vm_mount
vm_name=/forensicVM/mnt/vm/$name

cd "$vm_name"

function DismountImage {
     qemu-nbd --disconnect $first_nbd
     if [ $imagemanager == "ewf" ]; then
        umount "$image_ewf_mnt"
        echo "Dismounted $image_ewf_mnt"
     fi
     if [ $imagemanager == "aff" ]; then
        umount "$image_aff_mnt"
        echo "Dismounted $image_aff_mnt"

     fi
     sleep 5
}

function CleanUpINT {
     echo "CleanUp on errors"
     #qemu-nbd --disconnect "/dev/nbd0"
     qemu-nbd --disconnect $first_nbd
     if [ $imagemanager == "ewf" ]; then
        umount "$image_ewf_mnt"
     fi
     if [ $imagemanager == "aff" ]; then
        umount "$image_aff_mnt"
     fi
     rm "${vm_name}/S0001-P0000.qcow2-sda"
     read -p "Verify if the are any errors. Press any key to continue..."
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
     read -p "Now you can start the machine..."
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
   # TODO: Create an extra mount image to snapshot
fi

if [ $imagemanager == "aff" ]; then
   affuse -o direct_io "$image" "$image_aff_mnt"/
   if [[ $? -eq 0 ]]; then
       affrawmnt="${image_aff_mnt}/`ls $image_aff_mnt`"
       echo "Image mounted on: $affrawmnt"
       # TODO: Create an extra mount image to snapshot
   else
       echo "Error: could not mount $image"
       read -p ""
       exit 1
   fi
fi

tput bold
tput setaf 2
echo "3) Get image information"
tput sgr0

if [ $imagemanager == "qemu" ]; then
   virt-inspector "$1" > ${info_name}
fi

tput bold
tput setaf 2
echo "4) Create backing file snapshot"
tput sgr0
# shellcheck disable=SC2164
cd "$vm_name"
forensic_source=""
if [ $imagemanager == "ewf" ]; then
   qemu-img create -f qcow2 -b "$image_ewf_mnt"/ewf1 -F raw S0001-P0000.qcow2-sda
   forensic_source="$image_ewf_mnt"/ewf1
fi

if [ $imagemanager == "aff" ]; then
   echo "$affrawmnt"
   ls "$affrawmnt"
   qemu-img create -f qcow2 -b "$affrawmnt" -F raw S0001-P0000.qcow2-sda
   forensic_source="$affrawmnt"
fi

if [ $imagemanager == "qemu" ]; then
   qemu-img create -f qcow2 -b "$1" -F qcow2 S0001-P0000.qcow2-sda
   forensic_source="$1"
fi

tput bold
tput setaf 2




"$vm_name/S0002-P0001.qcow2-vnc.sh"

if [ $mode != "snap" ]; then
  tput bold
  tput setaf 2
  echo "9) Umounting paths"
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
  echo "10) Delete temp snapshot"
  tput sgr0
  rm "${vm_name}/S0001-P0000.qcow2-sda"
  echo "copy" > "${vm_name}/mode"
else
  DismountImage
  echo "snap" > "${vm_name}/mode"
fi
