<p align="center">
  <img src="/assets/banner.png" width="100%">
</p>

<p align="center">
  <a href="https://www.raspberrypi.com/products/"><img src="https://img.shields.io/badge/Tested%20on-Raspberry%20Pi%20-c51a4a" alt="Raspi"></a>
  <a href="https://www.raspberrypi.com/software/"><img src="https://img.shields.io/badge/supports-raspbian-red" alt="raspbian"></a>
  <a href="https://www.raspberrypi.com/software/"><img src="https://img.shields.io/badge/kernel-32bit%20%7C%2064bit-blue" alt="kernel"></a>  
  <a href="https://ubuntu.com/download/raspberry-pi"><img src="https://img.shields.io/badge/supports-ubuntu%20RT-orange" alt="ubuntu"></a>
  <a href="https://github.com/neurobionics/robot-ci/actions/workflows/build.yml"><img src="https://github.com/neurobionics/robot-ci/actions/workflows/build.yml/badge.svg" alt="build"></a>
</p>

**Robot CI**: Effortless building, testing, and deploying customized robot operating systems at scale. This tool lets you **version control your entire robot OS configuration and makes remote development a breeze**.

## 🎯 Key Features

This tool solves common challenges in robotics development:

| Feature | Description |
|---------|-------------|
| **Version-Controlled OS** | Track and manage your robot environment in code, enabling reproducible builds with GitHub Actions, and allowing for easy rollbacks and collaboration. |
| **Remote Development** | Provides optimized headless server images with automatic IP notifications via email, facilitating seamless remote development. |
| **Customizable Environment** | Allows for the pre-installation of drivers and custom packages, and the configuration of services and boot sequences to tailor the environment to specific needs. |
| **Network Auto-Config** | Automatically connects to WiFi networks and establishes a fallback access point when no WiFi networks are available, ensuring continuous connectivity. |

## 👥 Ideal for Developers Who
- Desire a **version-controlled robot environment**.
- Require **reproducible** development setups.
- Prefer **remote development** over manual Pi configuration.
- **Manage multiple robots** with similar configurations.

## 🛠️ Example Use Cases
- **Research labs** managing multiple test platforms or robots
- Robotics companies **deploying a fleet of robots**
- Educational institutions maintaining **student robots for course projects**
- Development teams needing **consistent robot environments** across multiple robots

> [!NOTE]
> Currently tested on Raspberry Pi 4 and 5. May not be compatible with Raspberry Pi Zero.

## 📝 Quick Start Guide

### 1. Use This Template
1. Click the "Use this template" button on the repository page to create a new repository based on this template.
2. Set up these secrets in your new repository under Actions and as repository secrets:

| Secret | Purpose |
|--------|---------|
| `EMAIL_ADDRESS` | Email address(es) to send notifications to; separate multiple addresses with commas **("," and not ", ")** |
| `ENTNETWORK_SSID` | Enterprise network name |
| `ENTNETWORK_IDENTITY` | Network username |
| `ENTNETWORK_PASSWORD` | Network password |
| `ENTNETWORK_PRIORITY` | Connection priority (>5 for enterprise) |
| `SMTP_SERVER` | SMTP server for email notifications, for Gmail use `smtp.gmail.com` |
| `SMTP_USERNAME` | Username for the email account that will send notifications |
| `SMTP_PASSWORD` | Password for the email account that will send notifications |

### 2. Build Your Image
1. Go to Actions tab → **Build a Robot Operating System**
2. Click **Run Workflow** and select your build options:
   - Choose device model, OS distribution, and architecture
   - Set hostname, username, and password
   - Configure WiFi settings for additional home networks
3. Once the build is complete, the OS image will be available as an artifact in the Actions tab.

### 3. Deploy & Connect
1. Download and flash the image to SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Boot your Pi
3. Connect via:
   - Enterprise or Home network: Check email for IP
   - Fallback AP mode: Connect to Pi's network (IP: 10.0.0.200)

## 🌐 Network Behavior

Network management is streamlined by [Robonet](https://github.com/neurobionics/robonet), our custom CLI tool designed to simplify network configuration and management.

Here's a brief overview of its functionality:

- **Primary Connection**: Automatically connects to prioritized WiFi networks.
- **Fallback Mode**: Establishes an access point with a static IP of `10.0.0.200` when no preferred networks are available.
- **IP Notification**: Sends an email notification with the device's IP address upon successful connection.

Read more about Robonet [here](https://github.com/neurobionics/robonet).

## 🤝 Contributing

All contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📜 License

This project is licensed under [Apache 2.0](LICENSE).

## 🐛 Issues

Found a bug or have a suggestion? Please [open an issue](https://github.com/neurobionics/robot-ci/issues).