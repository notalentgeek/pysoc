#!/bin/bash

cd ~/pysoc &&

yes | sudo apt-get update &&
yes | sudo apt-get upgrade &&

sudo chmod +x ~/pysoc/script/script-compile/* &&
sudo chmod +x ~/pysoc/script/script-setup/* &&
sudo ~/pysoc/script/script-compile/setup_ubuntu_1604_pyaudio.sh &&

yes | sudo pip3 -r ~/pysoc/req/req_ubuntu_1604.sh &&
sudo ~/pysoc/script/script-compile/compile_ubuntu_1604.sh &&

cd ~/