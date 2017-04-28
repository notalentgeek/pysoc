#!/bin/bash

cd /home/pi/pysoc
sudo rm -r /home/pi/pysoc/build /home/pi/pysoc/dist /home/pi/pysoc/__pycache__ /home/pi/pysoc/log ||
sudo pyinstaller --paths="/home/pi/pysoc/src" --paths="/home/pi/pysoc/src/cli" --paths="/home/pi/pysoc/src/collection-function" --paths="/home/pi/pysoc/src/config-and-database" --paths="/home/pi/pysoc/src/input" --onefile /home/pi/pysoc/pysoc.py &&
sudo chmod +x /home/pi/pysoc/dist/pysoc &&
sudo ln -s /home/pi/pysoc/dist/pysoc /bin