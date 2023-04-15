#!/bin/bash

# Show help if no arguments or if -h or --help are specified
if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 --windows-share <value> --share-login <value> --share-password <value> --replacement-share <value> --forensic-image-path <value> --folder-uuid <value> --copy [copy|snap]"
    exit 0
fi


# Parse command-line arguments
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --windows-share)
    windows_share="$2"
    shift # past argument
    shift # past value
    ;;
    --share-login)
    share_login="$2"
    shift # past argument
    shift # past value
    ;;
    --share-password)
    share_password="$2"
    shift # past argument
    shift # past value
    ;;
    --replacement-share)
    replacement_share="$2"
    shift # past argument
    shift # past value
    ;;
    --forensic-image-path)
    forensic_image_path="$2"
    shift # past argument
    shift # past value
    ;;
    --folder-uuid)
    folder_uuid="$2"
    shift # past argument
    shift # past value
    ;;
    --copy)
    copy="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    echo "Unknown option: $1"
    exit 1
    ;;
esac
done


# Mount the windows share
mount -t cifs "$windows_share" /mnt -o username="$share_login",password="$share_password"

# Run forensic2v script
/forensivVM/bin/forensic2v.sh "$forensic_image_path" "$folder_uuid" "$copy"

# Unmount the windows share
umount /mnt

# Replace the share with the replacement share
sed -i "s|$windows_share|$replacement_share|g" "$folder_uuid.vmdk"

pwd
cd /forensicVM
pwd
cd bin
pwd

# Test if file exists
if ! [ -e "/forensicVM/bin/forensic2v.sh" ]
then
  echo "File does not exist. Running commands..."
  # Run your commands here
  echo "Done."
else
  sudo ./forensic2v.sh
  echo "The forensicVM already exists. Mounting folder if necessary"
  if mount | grep -q "/forensicVM/mnt/vm/directory/mnt"; then
    echo "/forensicVM/mnt/vm/directory/mnt is mounted"
  else
    echo "/forensicVM/mnt/vm/directory/mnt is not mounted"
  fi
fi
