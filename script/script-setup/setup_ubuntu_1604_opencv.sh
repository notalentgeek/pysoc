#!/bin/bash

yes | sudo apt-get install build-essential cmake gfortran libatlas-base-dev libavcodec-dev libavformat-dev libgtk-3-dev libjasper-dev libjpeg8-dev libpng12-dev libswscale-dev libtiff5-dev libv4l-dev libx264-dev libxvidcore-dev pkg-config python2.7-dev python3.5-dev &&
cd ~ &&
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip &&
unzip opencv.zip &&
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip &&
unzip opencv_contrib.zip &&
cd ~/opencv-3.1.0/ &&
mkdir build &&
cd build &&
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
    -D BUILD_EXAMPLES=ON .. &&
make &&
sudo make install &&
sudo ldconfig &&
ln -s /usr/local/lib/python3.5/dist-packages/cv2.cpython-35m-x86_64-linux-gnu.so ~/pysoc/cv2.so