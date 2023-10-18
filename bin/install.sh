cp /forensicVM/etc/systemd/system/forensicvm /etc/systemd/system/forensicvm
systemctl daemon-reload
systemctl enable forensicvm
systemctl start forensicvm
