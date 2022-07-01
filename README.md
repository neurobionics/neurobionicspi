# CI Tool to Configure Embedded Hardware for Robotics
[![U-M](https://img.shields.io/badge/-University%20of%20Michigan-ffcb05)](https://umich.edu/)
[![Neurobionics](https://img.shields.io/badge/-Neurobionics-00274c)](https://neurobionics.robotics.umich.edu/)
[![RPi4](https://img.shields.io/badge/Tested%20on-Raspberry%20Pi%204B-c51a4a)](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
![Build](https://github.com/neurobionics/neurobionicspi/workflows/Build/badge.svg)

The purpose of this tool is to build an up-to-date image for a Raspberry Pi that can be used headless/GUI-less to control autonomous / remote robotic systems. It was built by the Neurobionics Lab at the University of Michigan to solve two major challenges: 1) maintaining a stable, consistent, working image for Raspberry Pis that foster robotics research; and 2) ease connectivity with local networks (e.g. U-M Wireless) to prevent use of 'internal lab networks.'  It is meant for people who wish to use a Raspberry Pi to control an intelligent / robotic system, where development is done remotely on a PC, and execution is run from the Raspberry Pi. In other words, this setup uses the Raspberry Pi like a microprocessor, and makes use of its networking, communications, and GPIO abilities. To access and program on the Raspberry Pi remotely, we use  [VSCode](https://code.visualstudio.com/download) or [WinSCP](https://winscp.net/eng/download.php)]; these programs also enable shared file transfer. 

The tool reconfigures an official [Raspbian distro](https://www.raspberrypi.com/software/operating-systems/) to include custom packages for robotics and automation, wireless connectivity to a known and configurable WiFi network, and it will create a fallback access point when the known wireless networks are not in range (fixed IP: 10.0.0.200). This enables usage of the same process and hardware when not in known Wifi network range (e.g. demos and conferences). The process installs libraries for communication, drivers for common sensors and ICs, the API for working with [Dephy products](dephy.com/faster/), and other modifications. 

While this image was originally configured for usage at the University of Michigan, it can be modified to connect to any set of known WiFi networks.  Hence, login in details for Michigan wireless must be obtained separately, through a document behind U-M login security. If you wish to use this image for locations/networks not at U-M, you can add your WiFi network details set in the workflow settings. 

This image has only been tested on the Raspberry Pi v4.  It will not work on the Raspberry Pi Zero.

<img src="https://github.com/neurobionics/neurobionicspi/blob/main/assets/neurobionicspi.PNG" width="1024">

# Features
* Uses [CI](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration) (Github Actions) to build a stable Raspbian image that is always up to date.
* When booted, the system will try to connect automatically to desired/configured WiFi networks in the build settings.
* Once connected to the network, it will email you its IP address from a U-M email account.
* If no known WiFi networks are in range, it will default to an access point configuraiton (broadcasting its own SSID), which is also conifured in in the build settings.
* Has a feature-rich [web interface](https://doxfer.webmin.com/Webmin/Introduction), which can be used to modify the networking setup and to run custom scripts.
* Provides a much easier way to build customized project-specific Raspbian images via Github Actions UI.
* Includes many pre-loaded Python libraries, but application-specific libraries may need to be added

\
<img src="https://github.com/neurobionics/neurobionicspi/blob/main/assets/interface.png">

# Usage
<img align="right" src="https://github.com/neurobionics/neurobionicspi/blob/main/assets/UI.PNG" width="400">

* `Fork` this repository to create your own private repository that shares the same default source code, which can then be customized.
* Navigate to the `Actions` tab in your forked repository.
* Select the `Build` workflow and click on `Run Workflow`
* Use the Github Actions pop-Up UI to modify the `hostname, username, password, AP SSID, AP passphrase and e-mail address(es)`.
* After a successful run, your custom Raspbian image will be attached as an artifact. You can download it by selecting the current workflow run and clicking on the attached `artifact`.
* Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or other softwares like [Etcher](https://www.balena.io/etcher/), [Rufus](https://rufus.ie/en/), etc to flash the downloaded image to a SD card.
* You can access the [web interface](https://doxfer.webmin.com/Webmin/Introduction) by entering the `IP address` of your RPi in a browser. **Login with your username and password from the workflow settings**.
* The static IP for the access point is 10.0.0.200.  If it boots into access point mode, you must use this IP address to connect wirelessly.  If it's in access point mode, you will see the SSID broadcast (SSID entered in the workflow settings)
* The location of the wpa supplicant file: ~/etc/wpa_supplicant/wpa_supplicant-wlan0.conf
* The location of the startup emailer script: ~/etc/startup_mailer.py
* The location of the Neurobionics ASCII banner: ~/home/pi/.bash_profile
* This image is meant for the Raspberry Pi 4.  It may work on other versions, but will not work on the Raspberry Pi Zero.

# Environment Variables

| Variable | Default Value |
| -------- | ------------- |
| `HOSTNAME` | neurobionicspi |
| `USER` | pi |
| `PASSWORD` | neurobionics |
| `AP_SSID` | NeurobionicsRPi |
| `AP_PASSPHRASE` | neurobionics |
| `WIFI_CC` | US |
| `WIFI_SSID` | Network |
| `WIFI_PASSPHRASE` | password |
| `EMAIL` | ejrouse@umich.edu | 

# Issues
Kindly report any issues [here](https://github.com/neurobionics/neurobionicspi/issues).

# References
* [Pimod](https://github.com/marketplace/actions/run-pimod)
