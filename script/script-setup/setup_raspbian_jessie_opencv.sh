#!/bin/bash

yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq-get purge wolfram-engine &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq-get install build-essential cmake gfortran libatlas-base-dev libavcodec-dev libavformat-dev libgtk2.0-dev libjasper-dev libjpeg-dev libpng12-dev libswscale-dev libtiff5-dev libv4l-dev libx264-dev libxvidcore-dev pkg-config python2.7-dev python3-dev &&
cd /home/pi &&
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip &&
unzip opencv.zip &&
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip &&
unzip opencv_contrib.zip &&
cd /home/pi/opencv-3.1.0/ &&
mkdir build &&
cd build &&
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/home/pi/opencv_contrib-3.1.0/modules \
    -D BUILD_EXAMPLES=ON .. &&
make &&
sudo make install &&
sudo ldconfig
ln -s /usr/local/lib/python3.4/dist-packages/cv2.cpython-34m.so /home/pi/pysoc/cv2.so