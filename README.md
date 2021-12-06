# Neurobionics Pi

Reconfigures an official [Raspbian distro](https://www.raspberrypi.com/software/operating-systems/) to include custom packages, connectivity to a wireless network, and to create a fallback access point when the configured wireless network can't be found, thereby automating the process of setting up a Raspberry Pi for Embedded Research.

# Features
* Uses [CI](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration) (Github Actions) to build a stable Raspbian image that is always up to date.
* Has a feature-rich [web interface](https://docs.raspap.com/), which can be used to modify the networking setup and to run custom scripts.
* Provides a much easier way to build customized project-specific Raspbian images via Github Actions UI.

# Usage
* Fork this repository to create your own private repository that shares the same default source code.
* Navigate to the ```Actions``` tab in your forked repository.
* Select the ```Build``` workflow and click on ```Run Workflow```
* Use the Github Actions pop-Up UI to modify the ```hostname,username, password, AP SSID, AP passphrase and e-mail address(es)```.
* After a successful run, your custom Raspbian image will be attached as an artifact. You can download it by selecting the current workflow run and clicking on the attached ```artifact```.
* Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or other softwares like [Etcher](https://www.balena.io/etcher/), [Rufus](https://rufus.ie/en/), etc to flash the downloaded image to a SD card.

# Environment Variables

# References
* [Pimod](https://github.com/marketplace/actions/run-pimod)
* [RaspAP](https://github.com/RaspAP/raspap-webgui)
