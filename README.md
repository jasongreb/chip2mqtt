# CHIP2MQTT: Update NTC C.H.I.P. Stats Over MQTT

The NTC C.H.I.P. was an inexpensive ARM-based board similar to the Raspberry Pi. It is a single core CPU with 512MB of RAM and storage built right
into the board. It included WiFi, Bluetooth, and a single USB port. This application will poll certain system variables and report them over MQTT.
This tool was primarily driven by the battery stats as the NTC C.H.I.P. also included a charge controller onboard.

## Requirements

While this utility is based on NTC C.H.I.P., it likely could be adapted for any system, including Raspberry Pi.

### Software

- Debian GNU/Linux 8 (jessie) - tested
- Python 3
- PAHO-MQTT for Python

## Install

### Clone Repo
Clone repo into opt

`cd /opt`

`sudo git clone https://github.com/jasongreb/chip2mqtt.git`

### Configure

Edit settings file and replace appropriate values for your configuration

`cd /opt/chip2mqtt`
`sudo nano /opt/chip2mqtt/settings.py`

### Install Service and Start

#### Run installservice.sh

Run bash script

`sudo /opt/chip2mqtt/installservice.sh`

#### Run commands manually

Copy chip2mqtt service configuration into systemd config

`sudo cp /opt/chip2mqtt/chip2mqtt.systemd.service /etc/systemd/system/chip2mqtt.service`

Refresh systemd configuration

`sudo systemctl daemon-reload`

Set chip2mqtt to run on startup

`sudo systemctl enable chip2mqtt.service`

Start chip2mqtt service

`sudo service chip2mqtt start`


