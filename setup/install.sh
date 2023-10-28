cd /
yes | git clone --recurse-submodules https://github.com/nunomourinho/forensicVM.git
cd /forensicVM/setup/apps
apt install -y dselect
bash restore.sh

cp /forensicVM/etc/systemd/system/forensicvm /etc/systemd/system/forensicvm
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
