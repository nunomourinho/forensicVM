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

# Flush existing rules
iptables -F
iptables -X

# Set default policies to ACCEPT
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

# Allow all traffic on default_gw
iptables -A INPUT -i $next_tap -s $default_route_gw -j ACCEPT
iptables -A OUTPUT -o $next_tap -d $default_route_gw -j ACCEPT

# Deny all local traffic on tap
iptables -A INPUT -i $next_tap -s 192.168.0.0/24 -j DROP
iptables -A OUTPUT -o $next_tap -d 192.168.0.0/24 -j DROP
iptables -A INPUT -i $next_tap -s 172.16.0.0/16 -j DROP
iptables -A OUTPUT -o $next_tap -d 172.16.0.0/16 -j DROP
iptables -A INPUT -i $next_tap -s 10.0.0.0/8 -j DROP
iptables -A OUTPUT -o $next_tap -d 10.0.0.0/8 -j DROP

# Allow all other traffic
iptables -A INPUT -i $next_tap -j ACCEPT
iptables -A OUTPUT -o $next_tap -j ACCEPT

echo "Bridge: $next_br"
echo "Tap: $next_tap"
echo "Interface: $default_route_interface"
echo "GW: $default_route_gw"
