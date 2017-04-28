#!/bin/bash

cd ~/pysoc
rm -r build dist __pycache__ log ||
pyinstaller --paths="./src" --paths="./src/cli" --paths="./src/collection-function" --paths="./src/config-and-database" --paths="./src/input" --onefile pysoc.py &&
chmod +x ~/pysoc/dist/pysoc &&
grep -q -F "PATH=\$PATH:~/pysoc/dist" ~/.bashrc || printf "PATH=\$PATH:~/pysoc/dist" >> ~/.bashrc
sudo ln -s ~/pysoc/dist/pysoc /usr/local/bin