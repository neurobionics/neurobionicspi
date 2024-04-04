<h2 align="center"><strong>neurobionicspi: A CI Tool to Configure Embedded Hardware for Robotics</strong></h2>

<p align="center">
  <a href="https://umich.edu/"><img src="https://img.shields.io/badge/-University%20of%20Michigan-ffcb05" alt="U-M"></a>
  <a href="https://neurobionics.robotics.umich.edu/"><img src="https://img.shields.io/badge/-Neurobionics-00274c" alt="Neurobionics"></a>
  <a href="https://www.raspberrypi.com/products/raspberry-pi-4-model-b/"><img src="https://img.shields.io/badge/Tested%20on-Raspberry%20Pi%204B-c51a4a" alt="RPi4"></a>
  <img src="https://github.com/neurobionics/neurobionicspi/workflows/Build/badge.svg" alt="Build">
</p>

The purpose of this tool is to build an up-to-date operating system/image for a Raspberry Pi that can be used headless/GUI-less to control autonomous / remote robotic systems. It was built by the Neurobionics Lab at the University of Michigan to solve two major challenges:

-   Maintaining a stable, consistent, working image for Raspberry Pis that fosters robotics research
-   Ease connectivity with local and enterprise networks to prevent use of internal lab networks

It is meant for developers or roboticists who wish to use a Raspberry Pi to control an intelligent / robotic system, where development is done remotely on a PC, and execution is run from the Raspberry Pi. In other words, this setup uses the Raspberry Pi like a microprocessor, and makes use of its networking, communications, and GPIO abilities. To access and program on the Raspberry Pi remotely, we use [VSCode](https://code.visualstudio.com) or [WinSCP](https://winscp.net/eng); these programs also enable shared file transfer.

<p align="center">
  <img src="/assets/neurobionicspi.PNG" width="800">
</p>

The tool reconfigures an official [Raspbian distro](https://www.raspberrypi.com/software/operating-systems/) to include custom packages for robotics and automation, wireless connectivity to a known and configurable WiFi network, and it will create a fallback access point when the known wireless networks are not in range (fixed IP: 10.0.0.200). This enables usage of the same process and hardware when not in known Wifi network range (e.g. demos and conferences). The process also installs libraries for communication, drivers for common sensors and ICs, APIs for working with [Dephy actuators](dephy.com/faster/) and other motors.

> [!NOTE]
> This image has only been tested on the Raspberry Pi 5 and 4. It may not work on the Raspberry Pi Zero.

# How to use this tool

## Step 1: Creating Secrets for Your Raspberry Pi Image

-   Start by creating your own copy of this repository. You can do this by clicking the `Fork` button. This will create a private repository in your GitHub account with the same default source code, which you can then customize to suit your needs.

-   Next, you need to create a few secrets in your repository. These secrets will be used to configure your Raspberry Pi image. To do this, navigate to the `Settings` tab in your repository, click on the `Secrets and Variables` dropdown link in the left sidebar, and then click on the `Actions` link.

-   Click on the `New repository secret` button and create the following secrets:

<div align="center">

| Secret Variable       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `EMAILS`              | Your email address or a comma-separated list of email addresses to receive the IP address of your Raspberry Pi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ENTNETWORK_SSID`     | The SSID/Name for your enterprise network.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `ENTNETWORK_IDENTITY` | The identity/username that can be used to connect to your enterprise network.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `ENTNETWORK_PASSWORD` | The password associated with the identity/username for your enterprise network.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `ENTNETWORK_PRIORITY` | This integer value determines the priority of the enterprise network. A higher value means higher priority. For example, if you have a home network and an enterprise network, and you want the Raspberry Pi to try connecting to the enterprise network first, you would give the enterprise network a higher priority number. If the enterprise network is not available, the Raspberry Pi will then attempt to connect to the network with the next highest priority. By default, the home network is assigned a priority of 5. If you want the Raspberry Pi to try connecting to the home network only if the enterprise network is not available, you would assign the enterprise network a priority higher than 5. |

</div>
-   If you are affiliated with the University of Michigan, we have created an account specifically for Raspberry Pis. You can find the credentials for this account [here](link-to-credentials).

-   If you are not affiliated with the University of Michigan and want your Raspberry Pi to connect to your university's WiFi network, please add your own enterprise network's information accordingly.

## Step 2: Building Your Raspberry Pi Image

-   After setting up the secrets, the next step is to build your custom Raspberry Pi image. This process is automated using a GitHub Actions workflow.

-   To start the build process, navigate to the `Actions` tab in your repository. This tab is located in the top menu of your repository page.

-   In the `Actions` tab, you'll see a single workflow named `Build Now!` in the left sidebar. This workflow is responsible for building your custom Raspbian image. Click on it to view more details.

-   On the workflow page, you'll see a `Run workflow` dropdown button on the right side of the page. Click on this button to open a form where you can enter additional configuration details for your Raspberry Pi image.
-   Fill in the following fields in the form. Fields marked with a red asterisk (\*) are required:

<div align="center">

| Field                         | Description                                                                 | Required |
| ----------------------------- | --------------------------------------------------------------------------- | -------- |
| `Device`                      | The type of Raspberry Pi device you are using.                              | Yes      |
| `Architecture`                | The architecture of your Raspberry Pi device.                               | Yes      |
| `Hostname`                    | The hostname for your Raspberry Pi.                                         | Yes      |
| `Username`                    | The username for your Raspberry Pi.                                         | Yes      |
| `Password`                    | The password for your Raspberry Pi.                                         | Yes      |
| `WiFi Country Code`           | The country code for your WiFi network.                                     | Yes      |
| `Additional Network SSID`     | The SSID of an additional network you want your Raspberry Pi to connect to. | No       |
| `Additional Network Password` | The password for the additional network.                                    | No       |
| `Access Point SSID`           | The SSID for the access point you want to create on your Raspberry Pi.      | No       |
| `Access Point Password`       | The password for the access point.                                          | No       |

</div>

-   After filling in these fields, click on the `Run workflow` button at the bottom of the form to start the build process. The workflow will use the secrets you've set up and the information you've just entered to customize your image.

-   The build process may take some time to complete. You can monitor its progress in the `Actions` tab. Once the build is complete, the workflow will create a custom Raspbian image and attach it as an artifact to the workflow run.

-   To download the image, go back to the `Actions` tab and click on the completed workflow run. You'll see a section labeled `Artifacts` on the bottom of the page. Click on the artifact to download your custom Raspbian image.

-   Once you've downloaded the image, you'll need to flash it onto an SD card. You can use software like [Raspberry Pi Imager](https://www.raspberrypi.com/software/), [Etcher](https://www.balena.io/etcher/), or [Rufus](https://rufus.ie/en/) to do this. Follow the instructions provided by the software to flash the image onto the SD card.

> [!IMPORTANT]
> If you're using the latest version of Raspberry Pi Imager, you'll be asked if you want to customize the OS. Please select 'No' to this option. The image you've built already contains the necessary customizations.

-   Once the image has been flashed onto the SD card, insert the card into your Raspberry Pi and power it on. The Raspberry Pi will boot up with the custom Raspbian image you've created. The initial boot may take a few minutes as the Raspberry Pi configures itself for the first time.

## Step 3: Connecting to Your Raspberry Pi

-   After flashing the image, insert the SD card into your Raspberry Pi. The Raspberry Pi will boot up with the custom image, and it will automatically connect to the networks you've configured using the secret variables and email you it's IP address if the network has internet access.

-   The static IP for the access point is 10.0.0.200. If it boots into access point mode, you must use this IP address to connect wirelessly. If it's in access point mode, you will see the SSID broadcast (SSID entered in the workflow settings)

# Helpful File Locations

-   WiFi network configuration file: `/etc/wpa_supplicant/wpa_supplicant-wlan0.conf`
-   IP address emailer script: `/etc/startup_mailer.py`
-   Welcome ASCII banner: `/home/pi/.bash_profile`

# Issues

Kindly report any issues [here](https://github.com/neurobionics/neurobionicspi/issues).

# References

-   [Pimod](https://github.com/marketplace/actions/run-pimod)
