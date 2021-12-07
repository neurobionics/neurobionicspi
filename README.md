# Neurobionics Pi
[![U-M](https://img.shields.io/badge/-University%20of%20Michigan-ffcb05)](https://umich.edu/)
[![Neurobionics](https://img.shields.io/badge/-Neurobionics-00274c)](https://neurobionics.robotics.umich.edu/)
[![RPi4](https://img.shields.io/badge/Tested%20on-Raspberry%20Pi%204B-c51a4a)](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
![Build](https://github.com/imsenthur/neurobionicspi/workflows/Build/badge.svg)

Reconfigures an official [Raspbian distro](https://www.raspberrypi.com/software/operating-systems/) to include custom packages, connectivity to a wireless network, and to create a fallback access point when the configured wireless network can't be found, thereby automating the process of setting up a Raspberry Pi for Embedded Research.

<img src="https://github.com/imsenthur/neurobionicspi/blob/main/assets/neurobionicspi.PNG" width="1024">

# Features
* Uses [CI](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration) (Github Actions) to build a stable Raspbian image that is always up to date.
* Has a feature-rich [web interface](https://docs.raspap.com/), which can be used to modify the networking setup and to run custom scripts.
* Provides a much easier way to build customized project-specific Raspbian images via Github Actions UI.

\
<img src="https://github.com/imsenthur/neurobionicspi/blob/main/assets/interface.PNG">

# Usage
<img align="right" src="https://github.com/imsenthur/neurobionicspi/blob/main/assets/UI.PNG">

* `Fork` this repository to create your own private repository that shares the same default source code, which can then be customized.
* Navigate to the `Actions` tab in your forked repository.
* Select the `Build` workflow and click on `Run Workflow`
* Use the Github Actions pop-Up UI to modify the `hostname, username, password, AP SSID, AP passphrase and e-mail address(es)`.
* After a successful run, your custom Raspbian image will be attached as an artifact. You can download it by selecting the current workflow run and clicking on the attached `artifact`.
* Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or other softwares like [Etcher](https://www.balena.io/etcher/), [Rufus](https://rufus.ie/en/), etc to flash the downloaded image to a SD card.
* You can access the Web interface by entering the IP address of your RPi in a browser.

| Web Interface | Default Value |
| -------- | ------------- |
| Username | `admin` |
| Password | `neurobionics` |

# Environment Variables

| Variable | Default Value |
| -------- | ------------- |
| `HOSTNAME` | neurobionicspi |
| `USER` | pi |
| `PASSWORD` | neurobionics |
| `AP_SSID` | NeurobionicsRPi |
| `AP_PASSPHRASE` | neurobionics |
| `EMAIL` | ejrouse@umich.edu | 

# Issues
Kindly report any issues [here](https://github.com/imsenthur/neurobionicspi/issues).

# References
* [Pimod](https://github.com/marketplace/actions/run-pimod)
* [RaspAP](https://github.com/RaspAP/raspap-webgui)
