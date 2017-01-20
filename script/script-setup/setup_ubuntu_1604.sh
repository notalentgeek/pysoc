#!/bin/bash

cd ~/pysoc &&

yes | sudo apt-get update &&
yes | sudo apt-get upgrade &&


sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_rpi_3.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_rpi_zero.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_ubuntu_1604.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_ubuntu_1604_opencv.sh &&
sudo chmod +x ~/pysoc/script/script-setup/setup_ubuntu_1604_server.sh &&

yes | sudo pip3 -r ~/pysoc/req/req_ubuntu_1604.sh
sudo ~/pysoc/script/script-compile/compile_ubuntu_1604.sh &&

cd ~/