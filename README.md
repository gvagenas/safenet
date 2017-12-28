# Safenet Application

Currently handling emergency situations for crowd big places such as shopping malls, schools or government buildings, is a short sighted process and the emergency handling authorities are lacking vital information for the situation.

A call to the emergency authorities to report an incident for a building, is not providing details such as which part of the building the incident is taking place and how many people are currently there.

For example, lets imagine a fire in the west side of the first floor of a shopping mall. An external observer would be able to just report a fire incident in the first floor of the shopping mall in the best case, but no details about a specific location of the building and how many people are currently there.

And here comes the Safenet application.

Safenet idea is based on the WiFi 802.11 Probe Request Frame and expands it to discover active devices in the range of a WiFi access point. The 802.11 Probe Request Frame is sent out by smartphones, laptops, and other devices that  are not currently connected to a WiFi network.Most smartphone devices send out this request every 40 to 60 seconds. The probe request frame will only contain MAC address and the distance of the device from the access point.

Given that most people now days carry at least their smartphone everywhere they go, and most of the times they don't switch off WiFi, we can safely assume that if we discover X devices, there are X people in the place. Safely assume means that small deviation on the number of persons reported from the actual number is insignificant, reporting 10 people instead of 11 or 12, makes no difference to the authorities.

Safenet is an edge computing application based on a mesh network of WiFi access points using Nodemcu ESP8266 (device edge), a mobile gateway based on Raspberry Pi Zero W and Hologram Nova (edge local processing) and Hologram Data Router (cloud).

## Installation

### Client

1. clone Safenet git repository to your local development environment (laptop): `git clone https://github.com/gvagenas/safenet.git Safenet`
1. Download and install Platform.io from http://platformio.org/
1. Open Platform.io and load Safenet/client application
1. Edit `main.ino` to provide the following:
  - `*client_ssid` The WiFi SSID that the ESP8266 will join to reach the mobile gateway
  - `*client_password` The WiFi password for the WiFi Access point
  - `mqtt_server` provide the IP Address of the Raspberry Pi (see server part)
  - Optionally you can provide `mqtt_port`, `mqtt_username` and `mqtt_password` as needed
1. Connect your Nodemcu unit and upload the firmware

Nodemcu now runs as both Access Point and Station mode, and will discover WiFi devices and will report them over MQTT to the mobile gateway that will be reached over the WiFi network that Station mode joined.

### Server

#### Part 1 - Prepare Raspberry Pi Zero W

1. Download Raspbian Stretch Lite - https://downloads.raspberrypi.org/raspbian_lite_latest
1. Use Etcher to burn image to SD card - https://etcher.io/
1. Mount SD card in your laptop and add `ssh` file onto the boot partition to enable SSH - https://www.raspberrypi.org/documentation/remote-access/ssh/
1. Mount SD card in your laptop and edit `/etc/wpa_supplicant/wpa_supplicant.conf` to add the Wifi details:
```
network={
    ssid="testing"
    psk="testingPassword"
}
```
1. Install SD Card to Raspberry Pi and power on the unit
1. SSH to Raspberr Pi using `ssh pi@raspberrypi.local`
1. Use `raspi-config` to expand filesystem
1. Update using `sudo apt-get update && sudo apt-get -y upgrade`
1. Install mosquito mqtt broker and client and git `sudo apt-get install -y mosquitto mosquitto-clients git`
1. Reboot using `sudo reboot`
1. Install Hologram python library `curl -L hologram.io/python-install | bash`
** At this step the Hologram installation script failed for me with `Cannot find python-sdk-auth. Please rerun the install script` and I had to manually add the missing library.** The extra steps are:
  * Install `python-sdk-auth` using `pip install python-sdk-auth==0.2.0`
  * Rerun hologram install script `curl -L hologram.io/python-install | bash`
  * Finally you will get:
`You are now ready to use the Hologram Python SDK!`
1. Test the Hologram Nova is working fine `sudo hologram send "Hello World"`

#### Part 2 - Install Safenet server Application

1. SSH to Raspberr Pi using `ssh pi@raspberrypi.local`
1. Clone application : `git clone https://github.com/gvagenas/safenet.git Safenet`
1. Change to the `Safenet/server` folder
1. Run `setup.sh` script to setup virtual environment and download required packages
1. Run application `run.sh` **Hologram Nova needs root privileges to use this interface**
