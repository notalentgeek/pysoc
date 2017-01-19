#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo pip3 install pyinstaller
sudo pip3 install virtualenv

curl -sS https://get.pimoroni.com/iotphat | bash

sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh
sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh
sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh
sudo chmod +x ~/pysoc/script/script-compile/compile_raspbian_jessie.sh.sh
sudo chmod +x ~/pysoc/script/script-compile/compile_ubuntu_1604.sh

~/setup_raspbian_jessie_lirc.sh
~/setup_raspbian_jessie_pyaudio.sh
~/setup_raspbian_jessie_usb_audio.sh

$SHELL