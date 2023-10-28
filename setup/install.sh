#!/bin/bash

cd /

REPO_URL="https://github.com/nunomourinho/forensicVM.git"
REPO_DIR="/forensicVM"

# Check if the repository directory exists
if [ -d "$REPO_DIR/.git" ]; then
    echo "Directory $REPO_DIR exists. Updating repository."
    cd "$REPO_DIR"
    git config pull.rebase false
    git pull
    git submodule update --init --recursive
else
    echo "Directory $REPO_DIR does not exist. Cloning repository."
    yes | git clone --recurse-submodules "$REPO_URL" "$REPO_DIR"
fi

cp /forensicVM/setup/apps/sources.list/sources.list /etc/apt/sources.list
apt update
apt upgrade -y

cd /forensicVM/setup
xargs -a /forensicVM/setup/installed_packages.txt apt install -y
cd /forensicVM/main/django-app
source /forensicVM/main/django-app/env_linux/bin/activate
pip install -r requirements_without_versions.txt

# Detect local IP address
local_ip=$(hostname -I | awk '{print $1}')

# Detect external IP address
external_ip=$(curl -s ipinfo.io/ip)

# Prepare the new ALLOWED_HOSTS line
new_allowed_hosts="ALLOWED_HOSTS = ['$local_ip', '$external_ip', 'localhost', '127.0.0.1']"
echo $new_allowed_hosts

# Replace the existing ALLOWED_HOSTS line in settings.py
sed -i "s/^ALLOWED_HOSTS = .*$/$new_allowed_hosts/" /forensicVM/main/django-app/conf/settings.py

cp /forensicVM/etc/systemd/system/forensicvm.service /etc/systemd/system/forensicvm.service
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
