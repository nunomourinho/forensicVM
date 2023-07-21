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
#next_br=$(find_next_available "br")
next_br=br0
next_tap=$(find_next_available "tap")
next_tap=tap1

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

modprobe br_netfilter
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables

iptables -P FORWARD ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

## Accept all other incoming and outgoing traffic, if it's related or established
iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# Allow all traffic on default_gw
iptables -A FORWARD -m physdev --physdev-in $next_tap -s $default_route_gw -j ACCEPT
iptables -A FORWARD -m physdev --physdev-out $next_tap -d $default_route_gw -j ACCEPT
iptables -A FORWARD -s $default_route_gw -j ACCEPT
iptables -A FORWARD -d $default_route_gw -j ACCEPT

# Drop all local traffic
iptables -A FORWARD -m physdev --physdev-out $next_tap -s 192.168.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -A FORWARD -m physdev --physdev-out $next_tap -s 172.16.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -A FORWARD -m physdev --physdev-out $next_tap -s 10.0.0.0/8 -d 192.168.0.0/16 -j DROP

iptables -A FORWARD -m physdev --physdev-out $next_tap -s 192.168.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -A FORWARD -m physdev --physdev-out $next_tap -s 172.16.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -A FORWARD -m physdev --physdev-out $next_tap -s 10.0.0.0/8 -d 172.16.0.0/12 -j DROP

iptables -A FORWARD -m physdev --physdev-out $next_tap -s 192.168.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -A FORWARD -m physdev --physdev-out $next_tap -s 172.16.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -A FORWARD -m physdev --physdev-out $next_tap -s 10.0.0.0/8 -d 10.0.0.0/8 -j DROP



iptables -A FORWARD -m physdev --physdev-in $next_tap -s 192.168.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -A FORWARD -m physdev --physdev-in $next_tap -s 172.16.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -A FORWARD -m physdev --physdev-in $next_tap -s 10.0.0.0/8 -d 192.168.0.0/16 -j DROP

iptables -A FORWARD -m physdev --physdev-in $next_tap -s 192.168.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -A FORWARD -m physdev --physdev-in $next_tap -s 172.16.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -A FORWARD -m physdev --physdev-in $next_tap -s 10.0.0.0/8 -d 172.16.0.0/12 -j DROP

iptables -A FORWARD -m physdev --physdev-in $next_tap -s 192.168.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -A FORWARD -m physdev --physdev-in $next_tap -s 172.16.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -A FORWARD -m physdev --physdev-in $next_tap -s 10.0.0.0/8 -d 10.0.0.0/8 -j DROP


# Accept remaining forwarded traffic
iptables -A FORWARD -j ACCEPT


# IPV6 Firewall
# The interface for the default route
default_route_interface_ipv6=$(ip -6 route | grep default | awk '{print $5}')
default_route_gw_ipv6=$(ip -6 route | grep default | awk '{print $3}')

ip6tables -P FORWARD ACCEPT
ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A OUTPUT -o lo -j ACCEPT

## Accept all other incoming and outgoing traffic, if it's related or established
ip6tables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
ip6tables -A OUTPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# Allow all traffic on default_gw_ipv6
ip6tables -A FORWARD -m physdev --physdev-in $next_tap -s $default_route_gw_ipv6 -j ACCEPT
ip6tables -A FORWARD -m physdev --physdev-out $next_tap -d $default_route_gw_ipv6 -j ACCEPT
ip6tables -A FORWARD -s $default_route_gw_ipv6 -j ACCEPT
ip6tables -A FORWARD -d $default_route_gw_ipv6 -j ACCEPT

# Drop all local traffic
ip6tables -A FORWARD -m physdev --physdev-out $next_tap -s fc00::/7 -d fc00::/7 -j DROP
ip6tables -A FORWARD -m physdev --physdev-out $next_tap -s fe80::/10 -d fc00::/7 -j DROP

ip6tables -A FORWARD -m physdev --physdev-in $next_tap -s fc00::/7 -d fc00::/7 -j DROP
ip6tables -A FORWARD -m physdev --physdev-in $next_tap -s fe80::/10 -d fc00::/7 -j DROP

# Accept remaining forwarded traffic
ip6tables -A FORWARD -j ACCEPT


echo "Bridge: $next_br"
echo "Tap: $next_tap"
echo "Interface: $default_route_interface"
echo "Interface: $default_route_interface_ipv6"
echo "GW: $default_route_gw"
echo "GW: $default_route_gw_ipv6"
