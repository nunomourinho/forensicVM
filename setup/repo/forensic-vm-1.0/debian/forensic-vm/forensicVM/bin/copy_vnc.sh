#!/bin/bash

# This script is a shell script written in Bash that is designed to convert forensic images into virtual machine images that can be run with QEMU, a virtualization software. The script starts by checking the command-line arguments passed to it, namely the path to the forensic image and the name of the virtual machine to be created. If any of these arguments is missing, the script displays an error message and exits.
# The script then proceeds to detect the image format of the forensic image, which could be in either qcow2, ewf, or aff format. It does this by using the 'qemu-img info' command to detect if the image is in qcow2 format, or by using the 'ewfinfo' and 'affinfo' commands to detect if it is in ewf or aff format respectively. If the format is not detected, the script displays an error message and exits.
# Next, the script mounts the forensic image using the appropriate command for the detected image format, and extracts information about the image using the 'virt-inspector' command. It then creates a snapshot of the image using the 'qemu-img create' command and sets up a block device using the 'qemu-nbd' command.
# The script then removes hibernate files from any mounted NTFS partitions in the snapshot using the 'ntfsfix' command, adds virtio drivers and QEMU guest agent to the snapshot using the 'virt-v2v' command, and modifies the QEMU startup script to include necessary parameters.
# If the script is run in 'copy' mode, it unmounts the mounted directories and deletes the temporary snapshot. If the script is run in 'snap' mode, it leaves the mounted directories and the temporary snapshot intact for later use. Finally, the script records the time it started and the time it ended, and calculates and displays the elapsed time.


# Record the start time
start_time=$(date +%s)

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

function change_qemu_vm {
   #echo "$5"
   startScript="#!/bin/bash

# Function to find the next available number for bridge and tap interfaces
find_next_available() {
     local base_name=\$1
     local i=0
     while ip link show \"\${base_name}\${i}\" >/dev/null 2>&1; do
        i=\$((i+1))
     done
     echo \"\${base_name}\${i}\"
}

tapInterface=\$(find_next_available \"tap\")
"

   vmconfig=$(cat "$1" | grep -v bash | grep -v /bin/sh | grep -v net0 | grep -v display | grep -v qxl | grep -v balloon | grep -v viosock | sed 's|format=raw|format=qcow2|g' | sed "s|cp '/usr/share/OVMF/OVMF_VARS.fd'|cp -n '/forensicVM/usr/share/qemu/OVMF_VARS.qcow2'|" | sed 's|/usr/share/OVMF/OVMF_CODE.fd|/forensicVM/usr/share/qemu/OVMF_CODE.qcow2|' | sed "s|\$uefi_vars|$5/OVMF_VARS.qcow2|")
   extra_parameters="-display vnc=0.0.0.0:\$1,websocket=\$2 \\
    -qmp unix:$3,server,nowait \\
    -pidfile $4 \\
    -usb -device usb-tablet -device usb-kbd \\
    -drive if=none,id=drive-ide0-0-0,readonly=on \\
    -device ide-cd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0 \\
    -vga virtio \\
    -drive file=evidence.qcow2,format=qcow2,if=virtio,index=1,media=disk \\
    -boot menu=on,strict=on,reboot-timeout=10000,splash-time=20000,splash=/forensicVM/branding/bootsplash.jpg \\
    -netdev tap,id=u1,ifname=\$tapInterface,script=/forensicVM/bin/start_tap.sh,downscript=/forensicVM/bin/end_tap.sh -device e1000,netdev=u1 -object filter-dump,id=f1,netdev=u1,file=$5/network.pcap"
    echo "$startScript
    $vmconfig
    $extra_parameters" >$2
    chmod 700 $2

}

echo "1) vm script"
echo "2) destination"
echo "3) websocket qmp/qmp.pid"
echo "4) pid"
echo "5) network"
change_qemu_vm $1 $2 "qmp/qmp.pid" "run/run.pid" "./network"
