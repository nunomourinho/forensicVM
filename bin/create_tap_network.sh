#!/bin/bash

apt install bridge-utils -y
apt install iptables -y
apt install -y uml-utilities

# Function to find the next available number for bridge and tap interfaces
find_next_available() {
    local base_name=$1
    local i=0
    while ip link show "${base_name}${i}" >/dev/null 2>&1; do
        i=$((i+1))
    done
    echo "${base_name}${i}"
}

# The interface for the default route
default_route_interface=$(route -n | grep 'UG[ \t]' | awk '{print $8}')
default_route_gw=$(route -n | grep 'UG[ \t]' | awk '{print $2}')

# Find next available bridge and tap interface
next_br=$(find_next_available "br")
next_tap=$(find_next_available "tap")

brctl addbr $next_br
ip tuntap add dev $next_tap mode tap user `whoami`
tunctl -u `whoami` -t $next_tap
brctl addif $next_br $next_tap
brctl addif $next_br $default_route_interface
ip link set $next_tap up promisc on
ip link set $next_tap down
ifconfig $next_br up
ifconfig $next_tap down

# Allow all traffic on default_gw
ufw allow in on $next_tap from $default_route_gw
ufw allow out on $next_tap from $default_route_gw

# Deny all traffic on tap from certain subnets
ufw deny in on $next_tap from 192.168.0.0/24
ufw deny out on $next_tap from 192.168.0.0/24
ufw deny in on $next_tap from 172.16.0.0/16
ufw deny out on $next_tap from 172.16.0.0/16
ufw deny in on $next_tap from 10.0.0.0/8
ufw deny out on $next_tap from 10.0.0.0/8

echo "Bridge: $next_br"
echo "Tap: $next_tap"
echo "Interface: $default_route_interface"
echo "GW: $default_route_gw"
