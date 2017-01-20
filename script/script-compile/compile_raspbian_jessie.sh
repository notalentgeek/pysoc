#!/bin/bash

sudo pyinstaller --paths="/home/pi/pysoc/src" --paths="/home/pi/pysoc/src/cli" --paths="/home/pi/pysoc/src/collection-function" --paths="/home/pi/pysoc/src/config-and-database" --paths="/home/pi/pysoc/src/input" --onefile /home/pi/pysoc/pysoc.py &&
sudo chmod +x /home/pi/pysoc/dist/pysoc &&
echo "PATH=$PATH:/home/pi/pysoc/dist" >> home/pi/.bash_profile &&
export PATH=$PATH:/home/pi/pysoc/dist &&
source home/pi/.bash_profile &&