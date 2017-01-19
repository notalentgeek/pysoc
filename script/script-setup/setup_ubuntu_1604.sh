#!/bin/bash

cd ~/pysoc

sudo apt-get update
sudo apt-get upgrade

sudo chmod +x /home/pi/pysoc/script/script-compile/compile_raspbian_jessie.sh
sudo chmod +x /home/pi/pysoc/script/script-compile/compile_ubuntu_1604.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh

sudo pip3 -r ~/pysoc/req/req_ubuntu_1604.sh
sudo chmod +x ~/pysoc/script/script-compile/compile_ubuntu_1604.sh
sudo ~/pysoc/script/script-compile/compile_ubuntu_1604.sh

$SHELL