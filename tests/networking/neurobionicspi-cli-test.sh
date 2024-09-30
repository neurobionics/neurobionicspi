entssid="MWireless"
networkconf="./network/08-wlan0-CLI.network"
conf_file="./wpa_supplicant-wlan0.conf"
emailer_script="./startup_mailer.py"
log_file="./neurobionicspi-cli.log"
count_file="./neurobionicspi-cli.count"

echo "" > ${log_file}
echo "0" > ${count_file}

cp ../../neurobionicspi-cli/neurobionicspi-cli ./neurobionicspi-cli
sed -i "s/entnetworkssid=\"\"/entnetworkssid=\"${entssid}\"/g" ./neurobionicspi-cli
sed -i "/^networkconf=/c\networkconf=\"${networkconf}\"" ./neurobionicspi-cli
sed -i "/^conf_file=/c\conf_file=\"${conf_file}\"" ./neurobionicspi-cli
sed -i "/^emailer_script=/c\emailer_script=\"${emailer_script}\"" ./neurobionicspi-cli
sed -i "/^log_file=/c\log_file=\"${log_file}\"" ./neurobionicspi-cli
sed -i "/^count_file=/c\count_file=\"${count_file}\"" ./neurobionicspi-cli

# replace systemctl restart systemd-networkd with a write to the log file with the same message
sed -i "/systemctl restart systemd-networkd/c\ \t\techo \"systemctl restart systemd-networkd\" >> ${log_file}" ./neurobionicspi-cli

# replace reconfigure_wpa_supplicant function with an empty function that logs a message
sed -i '/reconfigure_wpa_supplicant () {/,/}/c\reconfigure_wpa_supplicant () {\n    echo "reconfigure_wpa_supplicant function called" >> $log_file\n}' ./neurobionicspi-cli


bash ./neurobionicspi-cli  --help