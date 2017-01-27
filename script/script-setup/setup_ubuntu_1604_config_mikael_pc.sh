#!/bin/bash

cd ~/pysoc &&

yes | sudo apt-get update &&
yes | sudo apt-get upgrade &&

chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_picamera.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_rpi.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_rpi_config_elze.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_rpi_config_khiet.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_rpi_config_mikael.sh &&
chmod +x ~/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh &&
chmod +x ~/pysoc/script/script-setup/setup_ubuntu_1604.sh &&
chmod +x ~/pysoc/script/script-setup/setup_ubuntu_1604_opencv.sh &&
chmod +x ~/pysoc/script/script-setup/setup_ubuntu_1604_server.sh &&

yes | sudo pip3 -r ~/pysoc/req/req_ubuntu_1604.sh
sudo ~/pysoc/script/script-compile/compile_ubuntu_1604.sh &&

cp /home/pi/pysoc/premade-config/config_mikael_pc.ini /home/pi/pysoc/config.ini

cd ~/