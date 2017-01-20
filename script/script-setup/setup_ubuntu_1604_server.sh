#!/bin/bash

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list &&
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add - &&
sudo apt-get update &&

yes | sudo apt-get install python3 python3-pip rethinkdb &&
sudo cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance1.conf &&
sudo sed -ie "s/# bind=127.0.0.1/bind=all/g" /etc/rethinkdb/instances.d/instance1.conf &&

yes | sudo pip3 install -r ~/pysoc/req/requirement_ubuntu_1604_server.txt &&

printf "\nif netstat -an | grep -w \"29015\"; then\n    PORT_USED_DB=1\nelse\n    PORT_USED_DB=0\nfi\nif netstat -an | grep -w \"5000\"; then\n    PORT_USED_WEB=1\nelse\n    PORT_USED_WEB=0\nfi\nif [ \"\$PORT_USED_DB\" = \"0\" ]; then\n    sudo /etc/init.d/rethinkdb restart\nfi\nif [ \"\$PORT_USED_WEB\" = \"0\" ]; then\n    python3 -B ~/pysoc/pysoc_server.py 127.0.0.1 -o\nfi" >> ~/.bashrc &&

cd ~/ &&

sudo /etc/init.d/rethinkdb restart &&
python3 -B ~/pysoc/pysoc_server.py "$(curl ipinfo.io/ip)" -o