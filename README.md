<p align="center">
  <img src="/assets/banner.png" width="100%">
</p>

<p align="center">
  <a href="https://www.raspberrypi.com/products/"><img src="https://img.shields.io/badge/Tested%20on-Raspberry%20Pi%20-c51a4a" alt="Raspi"></a>
  <img src="https://github.com/neurobionics/neurobionicspi/actions/workflows/build.yml/badge.svg" alt="Build">
</p>

RoboPi: A CI tool for building, testing, and deploying customized robot operating systems at scale. This tool lets you version control your entire robot OS configuration and makes remote development a breeze.

## 🎯 Key Features

This tool solves common challenges in robotics development:

- **🔗 Version-Controlled OS**:
  - Track and manage your robot environment in code
  - Reproducible builds with GitHub Actions
  - Easy rollbacks and collaboration

- **🌐 Remote Development**:
  - Optimized headless server images
  - Automatic IP notifications via email

- **🔧 Customizable Environment**:
  - Pre-install drivers and custom packages
  - Configure services and boot sequences

- **📡 Network Auto-Config**:
  - Auto-connect to WiFi networks
  - Fallback access point when no WiFi networks are available

### Ideal for Developers Who:
- Desire a version-controlled robot environment.
- Require reproducible development setups.
- Prefer remote development over manual Pi configuration.
- Manage multiple robots with similar configurations.

> [!NOTE]
> Currently tested on Raspberry Pi 4 and 5. May not be compatible with Raspberry Pi Zero.

## 📝 Quick Start Guide

### 1. Fork & Configure
1. Fork this repository to your GitHub account
2. Set up required secrets in your fork:

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
1. Go to Actions tab → "Build Now!"
2. Configure your build:
   - Choose device model
   - Set hostname & credentials
   - Configure WiFi settings
3. Download the generated image

### 3. Deploy & Connect
1. Flash image to SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Boot your Pi
3. Connect via:
   - Enterprise/Home network: Check email for IP
   - Fallback AP mode: Connect to Pi's network (IP: 10.0.0.200)

## 🛠️ Technical Details

### Customization Options
- **Package Management**: 
  - Define exact versions of required packages
  - Add custom repositories
  - Include robot-specific drivers and libraries

- **Configuration Management**:
  - Custom boot sequences
  - Service configurations
  - Network settings
  - Development tools

- **Build Process**:
  - Based on official Raspbian distribution
  - Automated through GitHub Actions
  - Reproducible builds with version control
  - Custom post-installation scripts support

### Network Behavior
- **Primary**: Connects to configured WiFi networks by priority
- **Fallback**: Creates access point (static IP: 10.0.0.200)
- **Notification**: Emails IP address when online

### Example Use Cases
- Research labs managing multiple test platforms or robots
- Robotics companies deploying a fleet of robots
- Educational institutions maintaining student robots for course projects
- Development teams needing consistent robot environments across multiple robots

## 🤝 Contributing

All contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🐛 Issues

Found a bug or have a suggestion? Please [open an issue](https://github.com/neurobionics/neurobionicspi/issues).

## 📜 License
