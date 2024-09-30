#!/bin/bash

############################################
# Variables for systemd-networkd setup

wifi=wlan0
ethernet=eth0

############################################

# Re-enabling and installing classic networking

apt-mark unhold ifupdown dhcpcd5 isc-dhcp-client isc-dhcp-common rsyslog raspberrypi-net-mods openresolv
apt update
apt install -y ifupdown dhcpcd5 isc-dhcp-client isc-dhcp-common rsyslog

############################################

# Removing systemd-networkd configuration files

rm -f /etc/systemd/network/04-${ethernet}.network
rm -f /etc/systemd/network/08-${wifi}-CLI.network
rm -f /etc/systemd/network/12-${wifi}-AP.network

############################################

# Removing neurobionicspi-cli script

rm -f /usr/local/sbin/neurobionicspi-cli

############################################

# Removing systemd service for wpa_cli

if [ -f /etc/systemd/system/wpa_cli@${wifi}.service ] ; then
    systemctl disable wpa_cli@${wifi}.service
    rm -f /etc/systemd/system/wpa_cli@${wifi}.service
else
    echo "wpa_cli@$wifi.service is not installed"
fi

############################################

# Reverting changes to /etc/resolv.conf

rm -f /etc/resolv.conf
ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf

############################################

# Unholding packages

apt-mark unhold avahi-daemon libnss-mdns

############################################

# Disabling systemd services

systemctl disable systemd-networkd.service systemd-resolved.service

############################################

# Reloading systemd daemon

systemctl daemon-reload

echo "Uninstallation complete. Please reboot your device now by running this command: sudo reboot"
exit 0