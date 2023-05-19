#!/bin/bash

set -e

original_image="/dev/sda"
new_image="/path/to/new_image.qcow2"
additional_size="100M"

# Calculate sizes
original_size=$(stat -c %s "$original_image")
new_size=$((original_size + additional_size))

# Create the new qcow2 image
qemu-img create -f qcow2 "$new_image" "$new_size"

# Initialize the new image
guestfish -a "$new_image" <<EOF
run
part-add /dev/sda mbr
part-set-bootable /dev/sda 1 true
part-set-gpt-type /dev/sda 1 0x83
part-set-name /dev/sda 1 "Primary"
EOF

# Copy the contents of the original image to the new image
if qemu-nbd --connect=/dev/nbd0 "$new_image"; then
  if dd if="$original_image" of=/dev/nbd0p1 bs=4M status=progress; then
    qemu-nbd --disconnect /dev/nbd0
  else
    echo "Error: Failed to copy the contents of the original image."
    qemu-nbd --disconnect /dev/nbd0
    exit 1
  fi
else
  echo "Error: Failed to connect the new image to NBD."
  exit 1
fi

