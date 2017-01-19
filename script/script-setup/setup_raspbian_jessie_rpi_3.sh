#!/bin/bash

cd /home/pi/pysoc

sudo apt-get update
sudo apt-get upgrade
sudo pip3 install pyinstaller
sudo pip3 install virtualenv

sudo chmod +x /home/pi/pysoc/script/script-compile/compile_raspbian_jessie.sh
sudo chmod +x /home/pi/pysoc/script/script-compile/compile_ubuntu_1604.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh

sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh

sudo pip3 -r /home/pi/pysoc/req/req_raspbian_jessie.sh
sudo /home/pi/pysoc/script/script-compile/compile_raspbian_jessie.sh

$SHELL