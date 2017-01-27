#!/bin/bash

cd ~/pysoc &&

yes | sudo apt-get update &&
yes | sudo apt-get upgrade &&

sudo chmod +x ~/pysoc/script/script-compile/*
sudo chmod +x ~/pysoc/script/script-setup/*

yes | sudo pip3 -r ~/pysoc/req/req_ubuntu_1604.sh
sudo ~/pysoc/script/script-compile/compile_ubuntu_1604.sh &&

cp /home/pi/pysoc/premade-config/config_mikael_pc.ini /home/pi/pysoc/config.ini

cd ~/