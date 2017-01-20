#!/bin/bash

wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz -P /home/pi &&
tar xf /home/pi/pa_stable_v19_20140130.tgz -C /home/pi &&
cd /home/pi/portaudio &&
./configure &&
make &&
sudo make install &&
cd /home/pi &&
sudo /bin/sh -c 'printf "\nLD_LIBRARY_PATH=\"/usr/local/lib\"\nexport LD_LIBRARY_PATH\nLD_RUN_PATH=\"/usr/local/lib\"\nexport LD_RUN_PATH\nPATH=$PATH:/usr/local/lib/\nexport PATH" >> /home/pi/.bashrc'