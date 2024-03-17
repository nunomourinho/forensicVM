#!/bin/bash

msg_green() {
   tput bold
   tput setaf 2
   echo "$1"
   tput sgr0
}

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
  msg_green "This script must be run as root or with sudo privileges."
  exit 1
fi

# Check if rsync is installed, and install it if not
if ! [ -x "$(command -v rsync)" ]; then
  msg_green "Installing rsync."
  apt update
  apt install -y rsync sudo mc screen git curl wget
fi

cd /


msg_green "Updating git repository"
REPO_URL="https://github.com/nunomourinho/forensicVM.git"
REPO_DIR="/forensicVM"
TEMP_DIR="/forensicVM_git"

# Clone or update the repository in a temporary directory
if [ -d "$TEMP_DIR/.git" ]; then
    echo "Temporary directory $TEMP_DIR exists. Updating repository."
    cd "$TEMP_DIR"
    git config pull.rebase false
    git pull
    git submodule update --init --recursive
else
    msg_green "Temporary directory $TEMP_DIR does not exist. Cloning repository."
    yes | git clone --recurse-submodules "$REPO_URL" "$TEMP_DIR"
fi

# Sync files to the production directory, excluding settings.py
rsync -av --exclude '*/settings.py'--exclude '*/db.sqlite3' "$TEMP_DIR/" "$REPO_DIR/"

# Update submodules in the production directory
cd "$REPO_DIR"
git submodule update --init --recursive

msg_green "Updatating and upgrading installed packages"

cp /forensicVM/setup/apps/sources.list/sources.list /etc/apt/sources.list
apt update
apt upgrade -y

mkdir /forensicVM/mnt
mkdir /forensicVM/mnt/vm
mkdir /forensicVM/mnt/iso
mkdir /forensicVM/mnt/tmp



cd /forensicVM/setup
DEBIAN_FRONTEND=noninteractive
xargs -a /forensicVM/setup/installed_packages.txt apt install -y

msg_green "Installing python requirements"
cd /forensicVM/main/django-app
#rm -rf /forensicVM/main/django-app/env_linux
#python3 -m venv env_linux

#source /forensicVM/main/django-app/env_linux/bin/activate
pip install -r requirements_without_versions.txt


msg_green "Adding a forensic investigator user with a default password. Please change"
useradd -m forensicinvestigator
echo "forensicinvestigator:forensicinvestigator" | chpasswd

msg_green "Creating ssh keys - public and private"
username="forensicinvestigator"
# Create an SSH key pair for the user
if [ ! -f "/home/$username/.ssh/id_rsa" ]; then
  sudo -u "$username" ssh-keygen -t rsa -b 4096 -f "/home/$username/.ssh/id_rsa" -N ""
fi

# Create the authorized_keys file
touch "/home/$username/.ssh/authorized_keys"

# Create the known_hosts file
touch "/home/$username/.ssh/known_hosts"


# Set ownership and permissions for SSH files and directories
chown -R "$username:$username" "/home/$username/.ssh"
chmod 700 "/home/$username/.ssh"
chmod 600 "/home/$username/.ssh/authorized_keys"
chmod 644 "/home/$username/.ssh/known_hosts"

msg_green "User $username created with SSH keys and required files."


msg_green "Defining initial allowed hosts in django"
# Detect local IP address
local_ip=$(hostname -I | awk '{print $1}')

# Detect external IP address
external_ip=$(curl -s ipinfo.io/ip)

# Prepare the new ALLOWED_HOSTS line
new_allowed_hosts="ALLOWED_HOSTS = ['$local_ip', '$external_ip', 'localhost', '127.0.0.1']"
echo $new_allowed_hosts

# Replace the existing ALLOWED_HOSTS line in settings.py
sed -i "s/^ALLOWED_HOSTS = .*$/$new_allowed_hosts/" /forensicVM/main/django-app/conf/settings.py


msg_green "Adding extra /usr files"
# Define source and destination directories
source_dir="/forensicVM/usr/share"
destination_dir="/usr/share"

# Copy all files and folders recursively
cp -r "$source_dir"/* "$destination_dir"


msg_green "Patch qemu-img"
# Define the source and destination paths
source_path="/forensicVM/usr/bin/qemu-img"
destination_path="/usr/bin/qemu-img"

# Check if the source file exists
if [ -f "$source_path" ]; then
  # Check if the destination file exists and is different from the source
  if [ -f "$destination_path" ] && ! cmp -s "$source_path" "$destination_path"; then
    # Rename the destination file to .forensicVM
    mv "$destination_path" "$destination_path.forensicVM"
        
    if [ $? -eq 0 ]; then
      echo "Renamed $destination_path to $destination_path.forensicVM."
      cp "$destination_path.forensicVM" /forensicVM/usr/bin/qemu-img.forensicVM
    else
      echo "Error: Failed to rename $destination_path."
      exit 1
    fi
  fi

  # Copy the source file to the destination
  cp "$source_path" "$destination_path"
  if [ $? -eq 0 ]; then
    echo "Copied $source_path to $destination_path."
  else
    echo "Error: Failed to copy $source_path to $destination_path."
    exit 1
  fi
else
  echo "Error: Source file $source_path does not exist."
  exit 1
fi

msg_green "qemu-img sucessfully patched"

msg_green "Adding sudo forensicinvestigator actions"
# Define the line to add to sudoers
sudoers_line="forensicinvestigator ALL=(ALL) NOPASSWD: /forensicVM/bin/*, /forensicVM/plugins/*, /forensicVM/mnt/vm/*"

# Use visudo to edit the sudoers file
if ! grep -qF "$sudoers_line" /etc/sudoers; then
  echo "$sudoers_line" | sudo EDITOR='tee -a' visudo
  if [ $? -eq 0 ]; then
    echo "Line added to sudoers file successfully."
  else
    echo "Error: Failed to add line to sudoers file."
  fi
else
  echo "The line already exists in the sudoers file."
fi


msg_green "Reconfiguring shellinabox"
cp /forensicVM/etc/default/shellinabox /etc/default/shellinabox
systemctl daemon-reload
systemctl stop shellinabox
systemctl enable shellinabox
systemctl start shellinabox


msg_green "Installing and starting the forensicvm service"
cp /forensicVM/etc/systemd/system/forensicvm.service /etc/systemd/system/forensicvm.service
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
