#!/bin/bash

echo "$@"

# Show help if no arguments or if -h or --help are specified
if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 --windows-share <value> --share-login <value> --share-password <value> --replacement-share <value> --forensic-image-path <value> --folder-uuid <value> --copy [copy|snap]"
    exit 0
fi

echo "1)"

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
    --share-port)
    share_port="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    echo "Unknown option: $1"
    exit 1
    ;;
esac
done

echo "2)"

if ! [ -e "/forensicVM/mnt/vm/$folder_uuid/mode" ]
then
   echo "3)"
   mkdir /forensicVM/mnt/vm/$folder_uuid
   mkdir /forensicVM/mnt/vm/$folder_uuid/mnt
   # Mount the windows share
   mount -o username="$share_login",pass="$share_password",nobrl,ro,port=$share_port -t cifs "//127.0.0.1/$windows_share" "/forensicVM/mnt/vm/$folder_uuid/mnt"

   # Run forensic2v script
   /forensicVM/bin/forensic2v.sh "/forensicVM/mnt/vm/$folder_uuid/mnt/$forensic_image_path" "$folder_uuid" "$copy"
   umount /forensicVM/mnt/vm/$folder_uuid/mnt
fi
