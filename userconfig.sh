#!/bin/bash
set +e

if [ -f /usr/lib/userconf-pi/userconf ]; then
   /usr/lib/userconf-pi/userconf '${user}' '${hashedpwd}'
else
   echo "${user}:"'${hashedpwd}' | chpasswd -e
fi

if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_keymap 'us'
   /usr/lib/raspberrypi-sys-mods/imager_custom set_timezone 'America/Detroit'
else
  rm -f /etc/localtime
  echo "America/Detroit" >/etc/timezone
  dpkg-reconfigure -f noninteractive tzdata
  
  cat >/etc/default/keyboard <<'KBEOF'
  XKBMODEL="pc105"
  XKBLAYOUT="us"
  XKBVARIANT=""
  XKBOPTIONS=""
  KBEOF
  dpkg-reconfigure -f noninteractive keyboard-configuration
fi
