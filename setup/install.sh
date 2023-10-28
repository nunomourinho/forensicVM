cd /
yes | git clone --recurse-submodules https://github.com/nunomourinho/forensicVM.git
cd /forensicVM/setup
xargs -a /forensicVM/setup/installed_packages.txt apt install -y

cp /forensicVM/etc/systemd/system/forensicvm /etc/systemd/system/forensicvm
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
