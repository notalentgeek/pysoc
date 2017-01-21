#!/bin/bash

cd ~/pysoc
rm -r build dist __pycache__ log ||
pyinstaller --paths="./src" --paths="./src/cli" --paths="./src/collection-function" --paths="./src/config-and-database" --paths="./src/input" --onefile pysoc.py &&
sudo chmod +x ~/pysoc/dist/pysoc &&
sed -ie "s#PATH=PATH:~/pysoc/dist##g" ~/.bashrc &&
printf "\nPATH=\$PATH:~/pysoc/dist" >> ~/.bashrc &&
export PATH=$PATH:~/pysoc/dist