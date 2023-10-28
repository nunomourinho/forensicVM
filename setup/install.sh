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
cd /forensicVM/main/django-app
source /forensicVM/main/django-app/env_linux/bin/activate
pip install -r requirements_without_versions.txt

cp /forensicVM/etc/systemd/system/forensicvm.service /etc/systemd/system/forensicvm.service
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
