#!/bin/bash

cd /home/pi/pysoc &&

yes | sudo apt-get update &&
yes | sudo apt-get upgrade &&

sudo chmod +x /home/pi/pysoc/script/script-compile/*
sudo chmod +x /home/pi/pysoc/script/script-setup/*
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_prevent_screen_saver.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_lirc.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_picamera.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_pyaudio.sh &&
sudo /home/pi/pysoc/script/script-setup/setup_raspbian_jessie_usb_audio.sh &&

yes | sudo pip3 install -r /home/pi/pysoc/req/req_raspbian_jessie.txt &&
sudo /home/pi/pysoc/script/script-compile/compile_raspbian_jessie.sh &&

sudo /bin/sh -c 'printf "\nDISPLAY=:0 x-terminal-emulator --command \"sudo pysoc start\"" >> /home/pi/.bashrc' &&

cp /home/pi/pysoc/premade-config/config_khiet.ini /bin/config.ini &&
cp /home/pi/pysoc/premade-config/config_khiet.ini /home/pi/config.ini &&
cp /home/pi/pysoc/premade-config/config_khiet.ini /home/pi/pysoc/config.ini &&
cp /home/pi/pysoc/premade-config/config_khiet.ini /home/pi/pysoc/dist/config.ini &&

reboot