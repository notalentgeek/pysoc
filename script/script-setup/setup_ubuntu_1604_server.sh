#!bin/bash

adduser mikael
usermod -aG sudo mikael
su - mikael

git clone https://github.com/notalentgeek/pysoc

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install python3 python3-pip rethinkdb

sudo pip3 install -r ~/pysoc/req/requirement_ubuntu_1604_server.txt
rethinkdb --bind all &
python3 -B ~/pysoc/pysoc_server.py 37.139.9.247 &