#!/bin/bash

cd /home/pi/pysoc &&

yes | sudo apt-get update &&
yes | sudo apt-get upgrade &&

sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_picamera.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_rpi_3.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_rpi_zero.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_ubuntu_1604.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_ubuntu_1604_opencv.sh &&
sudo chmod +x /home/pi/pysoc/script/script-setup/setup_ubuntu_1604_server.sh &&

sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_picamera.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh &&

yes | sudo pip3 install -r /home/pi/pysoc/req/req_raspbian_jessie.txt &&
sudo /home/pi/pysoc/script/script-compile/compile_raspbian_jessie.sh &&

sudo /etc/init.d/lirc stop &&
timeout 2s mode2 -d /dev/lirc0 &&

reboot