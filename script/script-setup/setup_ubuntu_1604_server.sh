#!/bin/bash

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list &&
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add - &&
sudo apt-get update &&
yes | sudo apt-get install python3 python3-pip rethinkdb &&
yes | sudo pip3 install -r ~/pysoc/req/requirement_ubuntu_1604_server.txt &&
sudo cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance1.conf &&
sudo sed -ie "s/# bind=127.0.0.1/bind=all/g" /etc/rethinkdb/instances.d/instance1.conf &&
sudo /bin/sh -c 'printf "\nsudo /etc/init.d/rethinkdb restart" >> ~/.bashrc' &&
sudo /bin/sh -c 'printf "\npython3 -B ~/pysoc/pysoc_server.py "$(curl ipinfo.io/ip)" -o" >> ~/.bashrc' &&
source ~/.bashrc
