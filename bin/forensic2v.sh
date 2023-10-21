#!/bin/bash

# This script is a shell script written in Bash that is designed to convert forensic images into virtual machine images that can be run with QEMU, a virtualization software. The script starts by checking the command-line arguments passed to it, namely the path to the forensic image and the name of the virtual machine to be created. If any of these arguments is missing, the script displays an error message and exits.
# The script then proceeds to detect the image format of the forensic image, which could be in either qcow2, ewf, or aff format. It does this by using the 'qemu-img info' command to detect if the image is in qcow2 format, or by using the 'ewfinfo' and 'affinfo' commands to detect if it is in ewf or aff format respectively. If the format is not detected, the script displays an error message and exits.
# Next, the script mounts the forensic image using the appropriate command for the detected image format, and extracts information about the image using the 'virt-inspector' command. It then creates a snapshot of the image using the 'qemu-img create' command and sets up a block device using the 'qemu-nbd' command.
# The script then removes hibernate files from any mounted NTFS partitions in the snapshot using the 'ntfsfix' command, adds virtio drivers and QEMU guest agent to the snapshot using the 'virt-v2v' command, and modifies the QEMU startup script to include necessary parameters.
# If the script is run in 'copy' mode, it unmounts the mounted directories and deletes the temporary snapshot. If the script is run in 'snap' mode, it leaves the mounted directories and the temporary snapshot intact for later use. Finally, the script records the time it started and the time it ended, and calculates and displays the elapsed time.

forensic_dir=""
mkdir /forensicVM/mnt/vm/$2
mkdir /forensicVM/mnt/vm/$2/stats

tput bold
tput setaf 2
echo "Get disk stats - Please wait one minute..."
tput sgr0
fio --name=seq-write --rw=write --bs=4k --size=1G --directory=/forensicVM/mnt/tmp --runtime=60s --iodepth=32 --numjobs=1 --group_reporting=1 \
    --name=seq-read --rw=read --bs=4k --size=1G --directory=/forensicVM/mnt/tmp --runtime=60s --iodepth=32 --numjobs=1 --group_reporting=1 \
    --name=rand-write --rw=randwrite --bs=4k --size=1G --directory=/forensicVM/mnt/tmp --runtime=60s --iodepth=32 --numjobs=1 --group_reporting=1 \
    --name=rand-read --rw=randread --bs=4k --size=1G --directory=/forensicVM/mnt/tmp --runtime=60s --iodepth=32 --numjobs=1 --group_reporting=1 \
    --output-format=json --output=/forensicVM/mnt/vm/$2/stats/fio-stats.json

function extract_bandwidths_from_fio_output {
    # Check for input file argument
    if [[ $# -eq 0 ]]; then
        echo "Error: Please provide the path to the FIO JSON output file."
        return 1
    fi

    local FILE_PATH="$1/fio-stats.json"

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is not installed. Please install it to proceed."
        return 1
    fi

    # Extract bandwidth values using jq
    local READ_BW_KBPS=$(jq '.jobs[0].read.bw' "$FILE_PATH")
    local WRITE_BW_KBPS=$(jq '.jobs[0].write.bw' "$FILE_PATH")

    # Convert KB/s to MB/s
    local READ_BW_MBPS=$(echo "$READ_BW_KBPS / 1024" | bc -l)
    local WRITE_BW_MBPS=$(echo "$WRITE_BW_KBPS / 1024" | bc -l)

    # Print the results
    echo "$READ_BW_MBPS" > "$1/disk_read.txt"
    echo "$WRITE_BW_MBPS" > "$1/disk_write.txt"
}

benchmark_read_speed() {
    local file_path="$1"  # Input parameter: File path
    local size_to_read="2G"  # Size to read (e.g., 2GB)

    # Measure the time it takes to read the specified size from the file
    local start_time=$(date +%s.%N)
    dd if="$file_path" bs=1M count="$size_to_read" of=/dev/null
    local end_time=$(date +%s.%N)

    # Calculate the elapsed time in seconds
    local elapsed_time=$(echo "$end_time - $start_time" | bc)

    # Calculate the read speed in MB/s
    local read_speed=$(echo "scale=2; $size_to_read / $elapsed_time" | bc)

    echo "$read_speed" > "/forensicVM/mnt/vm/$2/stats/transfer_read_speed.txt"
}


benchmark_read_speed "/path/to/your/file"
extract_bandwidths_from_fio_output "/forensicVM/mnt/vm/$2/stats"




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

get_image_size() {
    # Get the argument (mount point)
    local mount_point="$1"

    # Check if the argument is provided
    if [ -z "$mount_point" ]; then
        echo "Error: Please provide the mount point."
        return 1
    fi

    # Find the associated loop device for the mount point
    local loop_device=$(df --output=source "$mount_point" | tail -1)

    # Check if the loop device was found
    if [ -z "$loop_device" ]; then
        echo "Error: No loop device found for mount point $mount_point"
        return 1
    fi

    # Get the backing file of the loop device
    local backing_file=$(losetup --noheadings --output=BACK-FILE "$loop_device")

    # Check if the backing file was found
    if [ -z "$backing_file" ]; then
        echo "Error: No backing file found for loop device $loop_device"
        return 1
    fi

    # Find the size of the backing file in bytes
    local file_size=$(stat --format=%s "$backing_file")

    # Return the file size
    echo "$file_size"
}



first_nbd=$(get_first_free_nbd)
first_nbd="/dev/nbd2"
echo $first_nbd
#read -p "pause"
#exit 1

# Helper function: Change qemu startup script.
# This is a Bash function that generates a modified QEMU virtual machine configuration file based on the input parameters.

# The function takes four arguments:

# $1 - the path to the original QEMU virtual machine configuration file
# $2 - the path to the output file where the modified configuration will be saved
# $3 - the path to the QEMU monitor socket
# $4 - the path to the PID file for the QEMU process
# $5 - the path of the vm
# The function first reads the original configuration file and filters out certain lines using grep. It # then replaces a path string using sed.
# The modified QEMU configuration includes additional parameters for the display, QEMU monitor, USB devices, VGA, and boot options. It also adds a read-only CD-ROM drive to the virtual machine.
# The modified configuration is then saved to the output file specified by $2. The file permissions are set to 700 to ensure that only the owner can execute it.

function change_qemu_vm {
   #echo "$5"

   missingScript="
qemu-system-x86_64 \\
    -no-user-config \\
    -nodefaults \\
    -name S0002-P0001.qcow2 \\
    -machine pc,accel=kvm:tcg \\
    -m 2048 \\
    -drive file=$5/S0002-P0001.qcow2-sda,format=qcow2,if=virtio,index=0,media=disk \\"

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

echo \$tapInterface > $5/tap.interface
"
   if [ -f "$1" ]; then
      vmconfig=$(cat "$1" | grep -v stdio | grep -v bash | grep -v /bin/sh | grep -v net0 | grep -v display | grep -v qxl | grep -v balloon | grep -v viosock | sed 's|format=raw|format=qcow2|g' | sed "s|cp '/usr/share/OVMF/OVMF_VARS.fd'|cp -n '/forensicVM/usr/share/qemu/OVMF_VARS.qcow2'|" | sed 's|/usr/share/OVMF/OVMF_CODE.fd|/forensicVM/usr/share/qemu/OVMF_CODE.qcow2|' | sed "s|\$uefi_vars|$5/OVMF_VARS.qcow2|")
   else
	vmconfig=$missingScript
        echo "Appending extra qemu init"
   fi
   extra_parameters="-display vnc=0.0.0.0:\$1,websocket=\$2 \\
    -serial stdio \\
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

function create_and_format_qcow2 {
    # Path to the new QCOW2 file
    qcow2_file="$1"

    # Create a new QCOW2 file with 20GB of space
    qemu-img create -f qcow2 $qcow2_file 20G

    # Name for the label
    label_name="possible evidence"

    # Create a new NTFS partition with guestfish
    guestfish --rw -a $qcow2_file <<EOF
    launch
#   part-init /dev/sda gpt
    part-init /dev/sda mbr
    part-add /dev/sda p 2048 -1024
    part-set-mbr-id /dev/sda 1 0x07
#   part-set-gpt-type /dev/sda 1 EBD0A0A2-B9E5-4433-87C0-68B6B72699C7
    mkfs ntfs /dev/sda1
    set-label /dev/sda1 "$label_name"
    mount /dev/sda1 /
#    mkdir /important001
#    mkdir /important002
#    mkdir /important003
    write /readme.txt "Forensic VM: This drive was automaticaly created. Please put the probable evidence inside the sub-folders with the same tag of autopsy software for the easyest classification"
    write /leiame.txt "Forensic VM: Este disco foi criado automáticamente. Para facilitar a classificação, por favor coloque as evidências recolhidas nas subpastas que têm o mesmo nome que a etiqueta no software autopsy"
    umount /
EOF
}

# Image is the complete path for the forensic image

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "Sintaxe: forensic2v <forensic-image> <name> [copy|snap]"
    read -p "Image not detected"
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
stats_dir=/forensicVM/mnt/vm/$name/stats
evidence_disk=/forensicVM/mnt/vm/$name/evidence.qcow2
forensic_dir=/forensicVM/mnt/vm/$name/

qmp_socket=$run_mount/qmp.sock
run_pid=$run_mount/run.pid
vm_mount=/forensicVM/mnt/vm
tmp_mount=$vm_mount
vm_name=/forensicVM/mnt/vm/$name
info_name=/forensicVM/mnt/vm/$name/${name}.info

echo $mode > "$stats_dir/mode"

if [ $mode == "snap" ]; then
   touch /tmp/qemu-img-cp-now
fi

mkdir "$vm_name"
mkdir "$image_ewf_mnt"
mkdir "$image_aff_mnt"
mkdir "$win_mount"
mkdir "$run_mount"
mkdir "$stats_dir"

function DismountImage {
     #qemu-nbd --disconnect "/dev/nbd0"
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
     echo $elapsed_time > "$stats_dir/conversion_time_in_seconds"
     echo "Elapsed time: $days days, $hours hours, $minutes minutes, $seconds seconds" > "$stats_dir/conversion_time_txt"
     read -p "Verify if the are any errors. Press any key to continue..."
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
   echo "ewf" > "$stats_dir/image_type"
fi

if [ $imagemanager == "aff" ]; then
   affuse -o direct_io "$image" "$image_aff_mnt"/
   if [[ $? -eq 0 ]]; then
       affrawmnt="${image_aff_mnt}/`ls $image_aff_mnt`"
       echo "Image mounted on: $affrawmnt"
       echo "aff" > "$stats_dir/image_type"
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
if [ $imagemanager == "ewf" ]; then
   filesize=$(stat -c "%s" "$image_ewf_mnt"/ewf1)
   echo $filesize > "$stats_dir/image_size"
   virt-inspector "$image_ewf_mnt"/ewf1 > ${info_name}
   # DEBUG: Comment bellow:
   #bash -i
fi

if [ $imagemanager == "aff" ]; then
   filesize=$(stat -c "%s" "$affrawmnt")
   echo $filesize > "$stats_dir/image_size"
   virt-inspector "$affrawmnt" > ${info_name}
   # DEBUG: Comment bellow:
   #bash -i
fi

if [ $imagemanager == "qemu" ]; then
   filesize=$(stat -c "%s" "$1")
   echo $filesize > "$stats_dir/image_size"
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




echo "5) Activate nbd block device"
tput sgr0
/sbin/modprobe nbd max_parts=25
qemu-nbd --connect=$first_nbd S0001-P0000.qcow2-sda
echo qemu-nbd --connect=$first_nbd S0001-P0000.qcow2-sda
#read -p "pause"
#qemu-nbd --connect=/dev/nbd0 S0001-P0000.qcow2-sda
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
   ntfsfix "${first_nbd}p$NUMBER"
   sync
   ntfsfix -d "${first_nbd}p$NUMBER"
   sync
   mount -t ntfs-3g "${first_nbd}p$NUMBER" "$win_mount" -o remove_hiberfile
   umount  "$win_mount"
   ntfsfix "${first_nbd}p$NUMBER"
   sync
   ntfsfix -d "${first_nbd}p$NUMBER"
done
qemu-nbd --disconnect "${first_nbd}"
sync


tput bold
tput setaf 2
echo "7) Add virtio drivers and qemu guest"
tput sgr0
virt-v2v -i disk "$vm_name/S0001-P0000.qcow2-sda"  -o qemu -of qcow2 -os "$vm_name" -on "S0002-P0001.qcow2"
#DEBUG
if [[ $? -eq 1 ]]; then
   check_disk_partitions "$forensic_source"
   exit_code=$?
   # Check if forrensic image has valid partions or is a single partion
   if [ $exit_code -eq 0 ]; then
      echo "Valid partitions detected. Copying image..."
      qemu-img convert -p -O qcow2 "$forensic_source" "$vm_name/S0002-P0001.qcow2-sda"
   else
      echo "Invalid partitions detected."
      tput bold
      tput setaf 2
      echo "Disk without partitions. Forensic image probably of a single partion. Heading to plan B..."
      echo "/forensicVM/bin/create-windows-partition.sh" "${vm_name}/temp_image.qcow2" $forensic_source ${vm_name}/S0002-P0001.qcow2
      tput sgr0
      /forensicVM/bin/create-windows-partition.sh "${vm_name}/temp_image.qcow2" $forensic_source ${vm_name}/S0002-P0001.qcow2
      #/forensicVM/bin/create-windows-partition.sh "${vm_name}/temp_image.qcow2" "$vm_name/S0001-P0000.qcow2-sda"  ${vm_name}/S0002-P0001.qcow2
      echo virt-v2v -i disk "${vm_name}/temp_image.qcow2" -o qemu -of qcow2 -os "$vm_name" -on "S0002-P0001.qcow2"
      virt-v2v -i disk "${vm_name}/temp_image.qcow2" -o qemu -of qcow2 -os "$vm_name" -on "S0002-P0001.qcow2"
      echo virt-inspector "${vm_image}/S0002-P0001.qcow2-sda" > ${info_name}
      virt-inspector "S0002-P0001.qcow2-sda" > ${info_name}
   fi
   #echo bash -i
   #bash -i
fi

change_qemu_vm "$vm_name/S0002-P0001.qcow2.sh" "$vm_name/S0002-P0001.qcow2-vnc.sh" "$qmp_socket" "$run_pid" "$vm_name"
qemu-img snapshot -c goldenSnapshot "$vm_name/S0002-P0001.qcow2-sda"

tput bold
tput setaf 2
echo "8) Create a evidence disk"
tput sgr0
# Create a evidence disk
create_and_format_qcow2 "${evidence_disk}"


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

