#!/bin/bash

sudo rm -r /home/pi/pysoc/build /home/pi/pysoc/dist /home/pi/pysoc/__pycache__ /home/pi/pysoc/log ||
sudo pyinstaller --paths="/home/pi/pysoc/src" --paths="/home/pi/pysoc/src/cli" --paths="/home/pi/pysoc/src/collection-function" --paths="/home/pi/pysoc/src/config-and-database" --paths="/home/pi/pysoc/src/input" --onefile /home/pi/pysoc/pysoc.py &&
sudo chmod +x /home/pi/pysoc/dist/pysoc &&
sudo sed -ie "s#\nPATH=\$PATH:~/pysoc/dist##g" ~/.bashrc &&
sudo /bin/sh -c 'printf "\nPATH=\$PATH:~/pysoc/dist" >> ~/.bashrc' &&
export PATH=$PATH:~/pysoc/dist &&
source ~/.bashrc