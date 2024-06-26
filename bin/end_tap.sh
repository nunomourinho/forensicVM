#!/bin/bash

# The interface for the default route
default_route_interface=br0
#$(route -n | grep 'UG[ \t]' | awk '{print $8}' | tail -n 1)
default_route_gw=$(route -n | grep 'UG[ \t]' | awk '{print $2}' | tail -n 1)

# Find next available bridge and tap interface
next_br=br0
next_tap=$1

# Get the uuid from the qemu command line
#uuid=$(ps -ef | grep qemu | grep $next_tap | awk -F '/' '{ for(i=1;i<=NF;i++) if ($i ~ /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/) print $i; exit}' | awk '{print $1}')
#uuid=$(ps -ef | grep qemu | grep $next_tap | awk -F '/' '{ for(i=1;i<=NF;i++) if ($i ~ /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/) {print $i; exit}}')
uuid=$(ps -ef | grep qemu | grep $next_tap | awk -F '/' '{ for(i=1;i<=NF;i++) if ($i ~ /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/) {print $i; exit}}')

echo $uuid

# Check if the pcap directory exists and create if not
if [[ ! -e /forensicVM/mnt/vm/${uuid}/pcap ]]; then
    mkdir -p /forensicVM/mnt/vm/${uuid}/pcap
fi

# Move the pcap file to the pcap directory
pcap_file_num=$(ls /forensicVM/mnt/vm/${uuid}/pcap/network*.pcap 2>/dev/null | wc -l)
new_pcap_file=$(printf "/forensicVM/mnt/vm/%s/pcap/network%04d.pcap" "$uuid" "$((pcap_file_num+1))")

if [[ -e /forensicVM/mnt/vm/${uuid}/network.pcap ]]; then
    mv /forensicVM/mnt/vm/${uuid}/network.pcap $new_pcap_file
fi

# Delete all traffic on default_gw
iptables -D FORWARD -m physdev --physdev-in $next_tap -s $default_route_gw -j ACCEPT
iptables -D FORWARD -m physdev --physdev-out $next_tap -d $default_route_gw -j ACCEPT
iptables -D FORWARD -s $default_route_gw -j ACCEPT
iptables -D FORWARD -d $default_route_gw -j ACCEPT

# Delete all local traffic
iptables -D FORWARD -m physdev --physdev-out $next_tap -s 192.168.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -D FORWARD -m physdev --physdev-out $next_tap -s 172.16.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -D FORWARD -m physdev --physdev-out $next_tap -s 10.0.0.0/8 -d 192.168.0.0/16 -j DROP

iptables -D FORWARD -m physdev --physdev-out $next_tap -s 192.168.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -D FORWARD -m physdev --physdev-out $next_tap -s 172.16.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -D FORWARD -m physdev --physdev-out $next_tap -s 10.0.0.0/8 -d 172.16.0.0/12 -j DROP

iptables -D FORWARD -m physdev --physdev-out $next_tap -s 192.168.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -D FORWARD -m physdev --physdev-out $next_tap -s 172.16.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -D FORWARD -m physdev --physdev-out $next_tap -s 10.0.0.0/8 -d 10.0.0.0/8 -j DROP

iptables -D FORWARD -m physdev --physdev-in $next_tap -s 192.168.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -D FORWARD -m physdev --physdev-in $next_tap -s 172.16.0.0/16 -d 192.168.0.0/16 -j DROP
iptables -D FORWARD -m physdev --physdev-in $next_tap -s 10.0.0.0/8 -d 192.168.0.0/16 -j DROP

iptables -D FORWARD -m physdev --physdev-in $next_tap -s 192.168.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -D FORWARD -m physdev --physdev-in $next_tap -s 172.16.0.0/16 -d 172.16.0.0/12 -j DROP
iptables -D FORWARD -m physdev --physdev-in $next_tap -s 10.0.0.0/8 -d 172.16.0.0/12 -j DROP

iptables -D FORWARD -m physdev --physdev-in $next_tap -s 192.168.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -D FORWARD -m physdev --physdev-in $next_tap -s 172.16.0.0/16 -d 10.0.0.0/8 -j DROP
iptables -D FORWARD -m physdev --physdev-in $next_tap -s 10.0.0.0/8 -d 10.0.0.0/8 -j DROP


# Delete remaining forwarded traffic
iptables -D FORWARD -j ACCEPT


# IPV6 Firewall
# The interface for the default route
default_route_interface_ipv6=br0
#$(ip -6 route | grep default | awk '{print $5}' | tail -n 1)
default_route_gw_ipv6=$(ip -6 route | grep default | grep "$default_route_interface_ipv6" | awk '{print $3}' | tail -n 1)
echo
echo
echo $default_route_gw_ipv6
echo
echo

# Allow all traffic on default_gw_ipv6
ip6tables -D FORWARD -m physdev --physdev-in $next_tap -s $default_route_gw_ipv6 -j ACCEPT
#echo "1"
ip6tables -D FORWARD -m physdev --physdev-out $next_tap -d $default_route_gw_ipv6 -j ACCEPT
#echo "2"
ip6tables -D FORWARD -s $default_route_gw_ipv6 -j ACCEPT
#echo "3"
ip6tables -D FORWARD -d $default_route_gw_ipv6 -j ACCEPT

# Drop all local traffic
ip6tables -D FORWARD -m physdev --physdev-out $next_tap -s fc00::/7 -d fc00::/7 -j DROP
#echo "4"
ip6tables -D FORWARD -m physdev --physdev-out $next_tap -s fe80::/10 -d fc00::/7 -j DROP
#echo "5"

ip6tables -D FORWARD -m physdev --physdev-in $next_tap -s fc00::/7 -d fc00::/7 -j DROP
#echo "6"
ip6tables -D FORWARD -m physdev --physdev-in $next_tap -s fe80::/10 -d fc00::/7 -j DROP
#echo "7"

# Accept remaining forwarded traffic
ip6tables -D FORWARD -j ACCEPT
#echo "8"

ip link set $next_tap down
brctl delif $next_br $next_tap
ip link delete $next_tap
#ip link set dev $default_route_interface master $next_br

echo "Bridge: $next_br"
echo "Tap: $next_tap"
echo "Interface IPV4: $default_route_interface"
echo "Interface IPV6: $default_route_interface_ipv6"
echo "GW IPV4: $default_route_gw"
echo "GW IPV6: $default_route_gw_ipv6"
exit 0
