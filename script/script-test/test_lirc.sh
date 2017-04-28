#!/bin/bash

sudo /etc/init.d/lirc stop
timeout 2s mode2 -d /dev/lirc0