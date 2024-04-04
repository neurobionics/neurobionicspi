<h2 align="center"><strong>neurobionicspi: A CI Tool to Configure Embedded Hardware for Robotics</strong></h2>

<p align="center">
  <a href="https://umich.edu/"><img src="https://img.shields.io/badge/-University%20of%20Michigan-ffcb05" alt="U-M"></a>
  <a href="https://neurobionics.robotics.umich.edu/"><img src="https://img.shields.io/badge/-Neurobionics-00274c" alt="Neurobionics"></a>
  <a href="https://www.raspberrypi.com/products/raspberry-pi-4-model-b/"><img src="https://img.shields.io/badge/Tested%20on-Raspberry%20Pi%204B-c51a4a" alt="RPi4"></a>
  <img src="https://github.com/neurobionics/neurobionicspi/workflows/Build/badge.svg" alt="Build">
</p>

<div style="border-width:1px;border-style:solid;border-radius:0.375rem;padding:1rem">
<p>
The purpose of this tool is to build an up-to-date operating system/image for a Raspberry Pi that can be used headless/GUI-less to control autonomous / remote robotic systems. It was built by the Neurobionics Lab at the University of Michigan to solve two major challenges:
</p>
<div style="border-width:1px;border-style:solid;border-radius:0.375rem;padding:0.75rem;margin:0.1rem">
Maintaining a stable, consistent, working image for Raspberry Pis that fosters robotics research
</div>
<div style="border-width:1px;border-style:solid;border-radius:0.375rem;padding:0.75rem;margin-left:0.1rem;margin-right:0.1rem;margin-bottom:1rem;margin-top:0.5rem">
Ease connectivity with local and enterprise networks to prevent use of internal lab networks
</div>
<p>
It is meant for developers or roboticists who wish to use a Raspberry Pi to control an intelligent / robotic system, where development is done remotely on a PC, and execution is run from the Raspberry Pi. In other words, this setup uses the Raspberry Pi like a microprocessor, and makes use of its networking, communications, and GPIO abilities. To access and program on the Raspberry Pi remotely, we use [VSCode](https://code.visualstudio.com/download) or [WinSCP](https://winscp.net/eng/download.php); these programs also enable shared file transfer.
</p>
</div>

The tool reconfigures an official [Raspbian distro](https://www.raspberrypi.com/software/operating-systems/) to include custom packages for robotics and automation, wireless connectivity to a known and configurable WiFi network, and it will create a fallback access point when the known wireless networks are not in range (fixed IP: 10.0.0.200). This enables usage of the same process and hardware when not in known Wifi network range (e.g. demos and conferences). The process installs libraries for communication, drivers for common sensors and ICs, the API for working with [Dephy products](dephy.com/faster/), and other modifications.

This image has only been tested on the Raspberry Pi 5 and 4. It may not work on the Raspberry Pi Zero.

<img src="https://github.com/neurobionics/neurobionicspi/blob/main/assets/neurobionicspi.png" width="1024">

# How to use this tool

<img align="right" src="https://github.com/neurobionics/neurobionicspi/blob/main/assets/UI.PNG" width="400">

-   `Fork` this repository to create your own private repository that shares the same default source code, which can then be customized.
-   Navigate to the `Actions` tab in your forked repository.
-   Select the `Build` workflow and click on `Run Workflow`
-   Use the Github Actions pop-Up UI to modify the `hostname, username, password, AP SSID, AP passphrase and e-mail address(es)`.
-   After a successful run, your custom Raspbian image will be attached as an artifact. You can download it by selecting the current workflow run and clicking on the attached `artifact`.
-   Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or other softwares like [Etcher](https://www.balena.io/etcher/), [Rufus](https://rufus.ie/en/), etc to flash the downloaded image to a SD card.
-   You can access the [web interface](https://doxfer.webmin.com/Webmin/Introduction) by entering the `IP address` of your RPi in a browser. **Login with your username and password from the workflow settings**.
-   The static IP for the access point is 10.0.0.200. If it boots into access point mode, you must use this IP address to connect wirelessly. If it's in access point mode, you will see the SSID broadcast (SSID entered in the workflow settings)
-   The location of the wpa supplicant file: `/etc/wpa_supplicant/wpa_supplicant-wlan0.conf`
-   The location of the startup emailer script: `/etc/startup_mailer.py`
-   The location of the Neurobionics ASCII banner: `/home/pi/.bash_profile`
-   This image is meant for the Raspberry Pi 4. It may work on other versions, but will not work on the Raspberry Pi Zero.

# Issues

Kindly report any issues [here](https://github.com/neurobionics/neurobionicspi/issues).

# References

-   [Pimod](https://github.com/marketplace/actions/run-pimod)
