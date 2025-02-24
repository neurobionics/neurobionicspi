<p align="center">
  <img src="/assets/banner.png" width="100%">
</p>

<p align="center">
  <a href="https://www.raspberrypi.com/products/"><img src="https://img.shields.io/badge/Tested%20on-Raspberry%20Pi%20-c51a4a" alt="Raspi"></a>
  <img src="https://img.shields.io/badge/supports-raspbian-red" alt="raspbian">
    <img src="https://img.shields.io/badge/kernel-32bit%20%7C%2064bit-blue" alt="kernel">
  <img src="https://img.shields.io/badge/supports-ubuntu%20RT-orange" alt="ubuntu">
  <img src="https://github.com/neurobionics/neurobionicspi/actions/workflows/build.yml/badge.svg" alt="build">
</p>

**RoboPi**: A CI tool for building, testing, and deploying customized robot operating systems at scale. This tool lets you **version control your entire robot OS configuration and makes remote development a breeze**.

## 🎯 Key Features

This tool solves common challenges in robotics development:

| Feature | Description |
|---------|-------------|
| **Version-Controlled OS** | - Track and manage your robot environment in code<br>- Reproducible builds with GitHub Actions<br>- Easy rollbacks and collaboration |
| **Remote Development** | - Optimized headless server images<br>- Automatic IP notifications via email |
| **Customizable Environment** | - Pre-install drivers and custom packages<br>- Configure services and boot sequences |
| **Network Auto-Config** | - Auto-connect to WiFi networks<br>- Fallback access point when no WiFi networks are available |

## 👥 Ideal for Developers Who
- Desire a **version-controlled robot environment**.
- Require **reproducible** development setups.
- Prefer **remote development** over manual Pi configuration.
- **Manage multiple robots** with similar configurations.

## 🛠️ Example Use Cases
- **Research labs** managing multiple test platforms or robots
- Robotics companies **deploying a fleet of robots**
- Educational institutions maintaining s**tudent robots for course projects**
- Development teams needing **consistent robot environments** across multiple robots

> [!NOTE]
> Currently tested on Raspberry Pi 4 and 5. May not be compatible with Raspberry Pi Zero.

## 📝 Quick Start Guide

### 1. Fork & Configure
1. Fork this repository to your GitHub account
2. Set up these secrets in your fork under Actions and as repository secrets:

| Secret | Purpose |
|--------|---------|
| `EMAIL_ADDRESS` | Email address(es) to send notifications to; separate multiple addresses with commas |
| `ENTNETWORK_SSID` | Enterprise network name |
| `ENTNETWORK_IDENTITY` | Network username |
| `ENTNETWORK_PASSWORD` | Network password |
| `ENTNETWORK_PRIORITY` | Connection priority (>5 for enterprise) |
| `SMTP_SERVER` | SMTP server for email notifications |
| `SMTP_USERNAME` | SMTP username for the email account that will send notifications |
| `SMTP_PASSWORD` | SMTP password for the email account that will send notifications |

### 2. Build Your Image
1. Go to Actions tab → "Build a Robot Operating System"
2. Configure your build:
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

### Network Behavior
Network behavior is managed by [Robonet](https://github.com/neurobionics/robonet), a CLI tool we developed with RUST to facilitate network configuration and management. 

- **Primary**: Connects to configured WiFi networks by priority
- **Fallback**: Creates access point (static IP: 10.0.0.200)
- **Notification**: Emails IP address when online

## 🤝 Contributing

All contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🐛 Issues

Found a bug or have a suggestion? Please [open an issue](https://github.com/neurobionics/neurobionicspi/issues).

## 📜 License
