#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo pip3 install pyinstaller
sudo pip3 install virtualenv

curl -sS https://get.pimoroni.com/iotphat | bash

sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh
sudo chmod +x /home/pi/pysoc/script/script-compile/compile_raspbian_jessie.sh
sudo chmod +x /home/pi/pysoc/script/script-compile/compile_ubuntu_1604.sh

sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh

$SHELL