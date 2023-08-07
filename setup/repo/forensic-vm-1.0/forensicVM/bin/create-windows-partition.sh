#!/bin/bash

#set -e

# Check if the correct number of arguments has been passed
if [ $# -ne 3 ]; then
    echo "Usage: $0 disk_image_base input_file output_name"
    exit 1
fi

# Check if input file exists and is readable
if [ ! -r "$2" ]; then
    echo "Error: Input file $2 does not exist or is not readable."
    exit 1
fi

# Check if the first argument is not empty
if [ -z "$1" ]; then
    echo "Error: The first argument must not be empty."
    exit 1
fi

# Check if the third argument is not empty
if [ -z "$3" ]; then
    echo "Error: The third argument must not be empty."
    exit 1
fi

# Check for necessary commands
for cmd in qemu-img guestfish qemu-nbd fdisk dd virt-v2v rm; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is not installed."
        exit 1
    fi
done

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

disk_image="$1"
base_size=$((($(stat -c%s "$2") / 1024 / 1024 / 1024)+5))  # base_size in GB
partition_image="/forensicVM/bin/win10bootp1.raw"

part_system_size=$((550 * 1024 * 1024))  # 550MB
part_windows_size=$(($base_size * 1024 * 1024 * 1024))  # base_size GB

# Calculate the total disk size
disk_size=$(($part_system_size + $part_windows_size))

# Create the disk image
qemu-img create -f qcow2 "$disk_image" "$disk_size"

# Start guestfish on the disk image
guestfish -a "$disk_image" <<EOF
# Launch the guestfish session
run

# Create the MBR partition table
part-init /dev/sda mbr

# Create the system partition
part-add /dev/sda p 2048 $(($part_system_size / 512))

# Create the Windows partition
part-add /dev/sda p $(($(($part_system_size / 512)) + 1)) $(($part_windows_size / 512))

# Mark the Windows partition as bootable
part-set-bootable /dev/sda 2 true
part-set-bootable /dev/sda 1 true

# Format the Windows partition as NTFS
mkfs ntfs /dev/sda1

# Format the Windows partition as NTFS
mkfs ntfs /dev/sda2

# Copy the partition image to the system partition
upload $partition_image /dev/sda1

# Quit guestfish
quit
EOF

qemu-nbd --connect=$first_nbd $disk_image
fdisk -lu /dev/nbd0
dd if=/forensicVM/bin/win10bootp1.raw of=/dev/nbd0p1 bs=4MB status=progress
dd if=$2 of=/dev/nbd0p2 bs=4MB status=progress
qemu-nbd --disconnect $first_nbd
/forensicVM/bin/remove-hibernation.sh $disk_image
#rm $disk_image
