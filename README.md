# BLE-Motor-Control
This projects uses the on board Bluetooth module of a Raspberry Pi to control a motor

## Required Materials

- [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)
- [DRV8825](https://www.amazon.com/HiLetgo-DRV8825-Stepper-RAMPS1-4-StepStick/dp/B01NCE3ZW1/ref=asc_df_B01NCE3ZW1/?tag=hyprod-20&linkCode=df0&hvadid=642160392949&hvpos=&hvnetw=g&hvrand=11448826655961308025&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9031300&hvtargid=pla-1892568611648&psc=1&gclid=CjwKCAjwyY6pBhA9EiwAMzmfwZ8FHHYLtlvce0gTeL1jkbKplZRfubvDAAiMaqLbF6CrmA9hkEAZeRoCuI8QAvD_BwE)
- [Stepper Motor](https://www.amazon.com/Nema17-Stepper-Motor-Bipolar-4-Lead/dp/B09SV33XS2/ref=asc_df_B09SV33XS2/?tag=hyprod-20&linkCode=df0&hvadid=632220147292&hvpos=&hvnetw=g&hvrand=4525797395312453952&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9031300&hvtargid=pla-1746500740006&th=1)

NOTE: The Raspberry Pi can be any model as long as there is a bluetooth module.  I just used a Raspberry Pi 3 model B I had laying around, so thats what I linked.
## Setup

This program should work cross platform but I ran this on Debian GNU/Linux 11 (bullseye) so the following steps reflect that setup process.

### Install BlueZ

1. Grab the latest BlueZ package link from the [offical website](http://www.bluez.org/download/)
1. Adjust the following code snippet to direct to the link copied from above
```shell
cd ~
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.66.tar.xz
tar xvf bluez-5.66.tar.xz
cd bluez-5.66
```
3. Install all dependencies
```shell
sudo apt-get update
sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
```
4. Configure BlueZ and make sure it finishes with no errors.  If there are errors then most likely there is a dependacy missing and needs to be installed
```shell
./configure --enable-library
```
5. Make and Install BlueZ
```shell
make
sudo make install
```
6. Enable Bluetooth service to run on boot
```shell
sudo systemctl enable bluetooth
```
7. Enable experimental mode by adding the '--experimental' flag to the bluetooth.service file
```shell
sudo nano /lib/systemd/system/bluetooth.service
```
```
[Unit]
Description=Bluetooth service
Documentation=man:bluetoothd(8)
ConditionPathIsDirectory=/sys/class/bluetooth

[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/local/libexec/bluetooth/bluetoothd --experimental //Change This Line              
NotifyAccess=main
#WatchdogSec=10
#Restart=on-failure
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
LimitNPROC=1

[Install]
WantedBy=bluetooth.target
Alias=dbus-org.bluez.service
```
8. Reload and restart the system
```shell
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
```
9. Check that everything is running with no errors and in experimental mode
```shell
systemctl status bluetooth
```

## Hardware

The following wiring will be setup based off a Raspbery Pi 3 model B and the DRV8825.

- 3.3v from Raspberry Pi to RST and SLP pin
- GND to GND
- Pin 21 to STEP
- Pin 20 to DIR
- Pin 14 to M0
- Pin 15 to M1
- Pin 18 to M2

The motor setup will be dependant on the motor but should be pretty straigt forward to set up.
## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## Refrences
- [BlueZ](http://www.bluez.org/)
- [Installing BlueZ Adafruit Guide](https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [Bleak](https://bleak.readthedocs.io/en/latest/)
- [rpimotorlib](https://pypi.org/project/rpimotorlib/)
- [Stepper Motor Control](https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/)