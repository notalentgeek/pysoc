#!/bin/bash
pyinstaller --paths="./src" --paths="./src/cli" --paths="./src/collection-function" --paths="./src/config-and-database" --paths="./src/input" --onefile pysoc.py
sudo chmod +x ~/pysoc/dist/pysoc
echo "PATH=$PATH:~/pysoc/dist" >> ~/.bash_profile
export PATH=$PATH:~/pysoc/dist
source ~/.bashrc
$SHELL