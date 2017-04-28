#!/bin/bash

cd ~/pysoc &&

yes | sudo apt-get update &&
yes | sudo apt-get upgrade &&

sudo chmod +x ~/pysoc/script/script-compile/* &&
sudo chmod +x ~/pysoc/script/script-setup/* &&
sudo ~/pysoc/script/script-compile/setup_ubuntu_1604_pyaudio.sh &&
sudo ~/pysoc/script/script-setup/setup_ubuntu_1604_opencv.sh &&

yes | sudo pip3 -r ~/pysoc/req/req_ubuntu_1604.sh &&
sudo ~/pysoc/script/script-compile/compile_ubuntu_1604.sh &&

sudo cp ~/pysoc/premade-config/config_mikael_pc.ini /bin/config.ini &&
sudo cp ~/pysoc/premade-config/config_mikael_pc.ini ~/config.ini &&
sudo cp ~/pysoc/premade-config/config_mikael_pc.ini ~/pysoc/config.ini &&
sudo cp ~/pysoc/premade-config/config_mikael_pc.ini ~/pysoc/dist/config.ini &&

cd ~/