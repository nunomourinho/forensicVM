#!/bin/bash

# Detect local IP address
local_ip=$(hostname -I | awk '{print $1}')

# Detect external IP address
external_ip=$(curl -s ipinfo.io/ip)

# Prepare the new ALLOWED_HOSTS line
new_allowed_hosts="ALLOWED_HOSTS = ['$local_ip', '$external_ip', 'localhost', '127.0.0.1']"
echo $new_allowed_hosts

# Replace the existing ALLOWED_HOSTS line in settings.py
#sed -i "s/^ALLOWED_HOSTS = .*$/$new_allowed_hosts/" /path/to/your/settings.py


