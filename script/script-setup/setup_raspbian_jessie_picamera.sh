#!/bin/bash

sudo sed -ie "/start_x=0/d" /boot/config.txt
sudo grep -q -F "start_x=1" /boot/config.txt || sudo /bin/sh -c 'printf "start_x=1" >> /boot/config.txt'
sudo grep -q -F "gpu_mem=128" /boot/config.txt || sudo /bin/sh -c 'printf "gpu_mem=128" >> /boot/config.txt'