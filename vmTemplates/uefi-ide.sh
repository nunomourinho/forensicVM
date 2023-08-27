#!/bin/bash


# Get the full path of the current script
SCRIPT_PATH="$(realpath $0)"

# Get the directory of the script
SCRIPT_DIR="$(dirname $SCRIPT_PATH)"

# Extract the UUID from the directory path
vmUUID="$(basename $SCRIPT_DIR)"


# Function to find the next available number for bridge and tap interfaces
find_next_available() {
     local base_name=$1
     local i=0
     while ip link show "${base_name}${i}" >/dev/null 2>&1; do
        i=$((i+1))
     done
     echo "${base_name}${i}"
}

tapInterface=$(find_next_available "tap")

echo $tapInterface > /forensicVM/mnt/vm/$vmUUID/tap.interface

    
# Make a copy of the UEFI variables template
uefi_vars="$(mktemp)"
cp -n '/forensicVM/usr/share/qemu/OVMF_VARS.qcow2' "/forensicVM/mnt/vm/$vmUUID/OVMF_VARS.qcow2"

qemu-system-x86_64 \
    -no-user-config \
    -nodefaults \
    -name S0002-P0001.qcow2 \
    -machine q35,accel=kvm:tcg \
    -drive if=pflash,format=qcow2,file=/forensicVM/usr/share/qemu/OVMF_CODE.qcow2,readonly \
    -drive if=pflash,format=qcow2,file="/forensicVM/mnt/vm/$vmUUID/OVMF_VARS.qcow2" \
    -m 4096 \
    -drive file=/forensicVM/mnt/vm/$vmUUID/S0002-P0001.qcow2-sda,format=qcow2,if=ide,index=0,media=disk \
    -object rng-random,filename=/dev/urandom,id=rng0 \
    -device virtio-rng-pci,rng=rng0 \
    -device pvpanic,ioport=0x505 \
    -display vnc=0.0.0.0:$1,websocket=$2 \
    -qmp unix:/forensicVM/mnt/vm/$vmUUID/run/qmp.sock,server,nowait \
    -pidfile /forensicVM/mnt/vm/$vmUUID/run/run.pid \
    -usb -device usb-tablet -device usb-kbd \
    -drive if=none,id=drive-ide1-0-0,readonly=on \
    -device ide-cd,bus=ide.1,unit=0,drive=drive-ide1-0-0,id=ide1-0-0 \
    -vga virtio \
    -drive file=evidence.qcow2,format=qcow2,if=ide,index=2,media=disk \
    -boot menu=on,strict=on,reboot-timeout=10000,splash-time=20000,splash=/forensicVM/branding/bootsplash.jpg \
    -netdev tap,id=u1,ifname=$tapInterface,script=/forensicVM/bin/start_tap.sh,downscript=/forensicVM/bin/end_tap.sh -device e1000,netdev=u1 -object filter-dump,id=f1,netdev=u1,file=/forensicVM/mnt/vm/$vmUUID/network.pcap
