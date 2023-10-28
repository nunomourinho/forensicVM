cd /
ssh-keyscan github.com >> ~/.ssh/known_hosts
yes | git clone --recurse-submodules https://github.com/nunomourinho/forensicVM.git /


cp /forensicVM/etc/systemd/system/forensicvm /etc/systemd/system/forensicvm
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
