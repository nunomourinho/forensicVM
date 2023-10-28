#!/bin/bash

cp /forensicVM/setup/apps/sources.list/sources.list /etc/apt/sources.list
apt update
apt upgrade -y
cd /

REPO_URL="https://github.com/nunomourinho/forensicVM.git"
REPO_DIR="forensicVM"

# Check if the repository directory exists
if [ -d "$REPO_DIR/.git" ]; then
    echo "Directory $REPO_DIR exists. Updating repository."
    cd "$REPO_DIR"
    git pull origin master
    git submodule update --init --recursive
else
    echo "Directory $REPO_DIR does not exist. Cloning repository."
    yes | git clone --recurse-submodules "$REPO_URL" "$REPO_DIR"
fi
cd /forensicVM/setup
xargs -a /forensicVM/setup/installed_packages.txt apt install -y

cp /forensicVM/etc/systemd/system/forensicvm /etc/systemd/system/forensicvm
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
