#!/bin/bash

############################################
# Variables for systemd-networkd setup

wifi=wlan0
ethernet=eth0
ipaddress=10.0.0.200/24

############################################

# Switching to systemd-networkd, read more at https://raspberrypi.stackexchange.com/questions/108592
# Uninstalling classic networking

apt --autoremove -y purge ifupdown dhcpcd5 isc-dhcp-client isc-dhcp-common rsyslog
apt-mark hold ifupdown dhcpcd5 isc-dhcp-client isc-dhcp-common rsyslog raspberrypi-net-mods openresolv
rm -r /etc/network /etc/dhcp

############################################

# Setting up systemd-networkd network manager

apt --autoremove -y purge avahi-daemon
apt-mark hold avahi-daemon libnss-mdns
ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
systemctl enable systemd-networkd.service systemd-resolved.service

############################################

# Writing configuration files for systemd-networkd

cat > /etc/systemd/network/04-${ethernet}.network <<-EOF
	[Match]
	Name=$ethernet
	[Network]
	DHCP=yes
	MulticastDNS=yes
EOF

cat > /etc/systemd/network/08-${wifi}-CLI.network <<-EOF
	[Match]
	Name=$wifi
	[Network]
	DHCP=yes
	MulticastDNS=yes
EOF
		
cat > /etc/systemd/network/12-${wifi}-AP.network <<-EOF
	[Match]
	Name=$wifi
	[Network]
	Address=$ipaddress
	IPForward=yes
	IPMasquerade=yes
	DHCPServer=yes
	MulticastDNS=yes
	[DHCPServer]
	DNS=1.1.1.1
EOF

cp $(pwd)/automagic-ap /usr/local/sbin/
chmod +x /usr/local/sbin/automagic-ap

############################################

# Installing systemd-service

if [ ! -f /etc/systemd/system/wpa_cli@${wifi}.service ] ; then
	cat > /etc/systemd/system/wpa_cli@${wifi}.service <<-EOF
		[Unit]
		Description=automagic-ap creates an wireless access point if known networks cannot be found.
		After=wpa_supplicant@%i.service
		BindsTo=wpa_supplicant@%i.service
		[Service]
		ExecStart=/sbin/wpa_cli -i %I -a /usr/local/sbin/automagic-ap
		Restart=on-failure
		RestartSec=1
		[Install]
		WantedBy=multi-user.target
	EOF
else
  echo "wpa_cli@$wifi.service is already installed"
fi

############################################

# Enabling systemd-service

systemctl daemon-reload
systemctl enable wpa_cli@${wifi}.service
echo "Reboot now!"
exit 0
