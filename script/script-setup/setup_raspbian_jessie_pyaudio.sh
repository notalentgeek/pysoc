#!/bin/bash

wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
tar xf pa_stable_v19_20140130.tgz
cd portaudio/
./configure
make
sudo make install
cd ~
printf "\nLD_LIBRARY_PATH=\"/usr/local/lib\"\nexport LD_LIBRARY_PATH\nLD_RUN_PATH=\"/usr/local/lib\"\nexport LD_RUN_PATH\nPATH=$PATH:/usr/local/lib/\nexport PATH" >> ~/.bashrc