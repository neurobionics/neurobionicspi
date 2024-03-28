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
		Description=Creates an wireless access point if known networks are unreachable.
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

# Check if the MWireless network block exists in the configuration file
if grep -q "ssid=\"MWireless\"" /etc/wpa_supplicant/wpa_supplicant-wlan0.conf; then
	# Find the line number of the MWireless network block start
	start_line=$(grep -n "ssid=\"MWireless\"" /etc/wpa_supplicant/wpa_supplicant-wlan0.conf | cut -d ":" -f 1)

	# Find the line number of the MWireless network block end
	end_line=$(grep -n "}" /etc/wpa_supplicant/wpa_supplicant-wlan0.conf | awk -v start=$start_line '$1 > start {print $1; exit}' | awk -F ":" '{print $1}')
	duplicate_start_line=$((start_line - 2))
	priority_line=$((start_line - 1))

	# Add a newline at the beginning and end of the duplicated network block
	sed -n "${duplicate_start_line},${end_line}p" /etc/wpa_supplicant/wpa_supplicant-wlan0.conf | sed '1s/^/\n/;$s/$/\n/' >> /etc/wpa_supplicant/wpa_supplicant-wlan0.conf

	original_priority=$(sed -n "${priority_line}p" /etc/wpa_supplicant/wpa_supplicant-wlan0.conf | awk -F "=" '{print $2}' | tr -d ' ')

	new_priority=$((original_priority + 1))
	# Update the priority in the duplicated network block
	sed -i "${duplicate_start_line},${end_line}s/priority=$original_priority/priority=$new_priority/" /etc/wpa_supplicant/wpa_supplicant-wlan0.conf

	echo "Duplicated MWireless network block and appended it to the end of your network configuration."
else
	echo "MWireless network block not found in the configuration file. Skipping duplication."
fi

# Enabling systemd-service

systemctl daemon-reload
systemctl enable wpa_cli@${wifi}.service
echo "Reboot now!"
exit 0
