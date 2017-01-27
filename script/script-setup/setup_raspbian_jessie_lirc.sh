#!/bin/bash

# Install LIRC packages for Raspbian Jessie.
yes | sudo apt-get install lirc liblircclient-dev &&
# Add pinouts mapping into `/etc/modules`.
sudo /bin/sh -c 'printf "\n\nlirc_dev\nlirc_rpi gpio_in_pin=23 gpio_out_pin=22" >> /etc/modules' &&
# Deleting `hardware.conf` and then re - create it back.
sudo rm /etc/lirc/hardware.conf &&
sudo /bin/sh -c 'printf "\n########################################################\n# /etc/lirc/hardware.conf\n#\n# Arguments which will be used when launching lircd\nLIRCD_ARGS=\"--uinput\"\n\n# Do not start lircmd even if there seems to be a good config file\n# START_LIRCMD=false\n\n# Do not start irexec, even if a good config file seems to exist.\n# START_IREXEC=false\n\n# Try to load appropriate kernel modules\nLOAD_MODULES=true\n\n# Run \"lircd --driver=help\" for a list of supported drivers.\nDRIVER=\"default\"\n# usually /dev/lirc0 is the correct setting for systems using udev\nDEVICE=\"/dev/lirc0\"\nMODULES=\"lirc_rpi\"\n\n# Default configuration files for your hardware if any\nLIRCD_CONF=\"\"\nLIRCMD_CONF=\"\"\n########################################################" > /etc/lirc/hardware.conf' &&
# Add line into boot configuration.
sudo /bin/sh -c 'printf "\ndtoverlay=lirc-rpi,gpio_in_pin=23,gpio_out_pin=22" >> /boot/config.txt' &&
# Backup the original IR codes dictionary and then add our own.
sudo mv /etc/lirc/lircd.conf /etc/lirc/lircd_backup.conf &&
sudo /bin/sh -c 'printf "\n# Please make this file available to others\n# by sending it to <lirc@bartelmus.de>\n#\n# this config file was automatically generated\n# using lirc-0.9.0-pre1(default) on Sat Jan  7 22:45:56 2017\n#\n# contributed by \n#\n# brand:                       /home/pi/lircd.conf\n# model no. of remote control: \n# devices being controlled by this remote:\n#\nbegin remote\n  name  pysoc\n  bits           13\n  flags RC5|CONST_LENGTH\n  eps            30\n  aeps          100\n  one           924   840\n  zero          924   840\n  plead         970\n  gap          113287\n  toggle_bit_mask 0x0\n      begin codes\n          KEY_1                    0x1001\n          KEY_2                    0x1002\n          KEY_3                    0x1003\n      end codes\nend remote" > /etc/lirc/lircd.conf' &&
# Add local and system wide `lircrc`.
sudo /bin/sh -c 'printf "\nbegin\n    button = KEY_1\n    config = KEY_1\n    prog = pysoc\nend\nbegin\n    button = KEY_2\n    config = KEY_2\n    prog = pysoc\nend\nbegin\n    button = KEY_3\n    config = KEY_3\n    prog = pysoc\nend" > /home/pi/.lircrc' &&
sudo /bin/sh -c 'printf "\nbegin\n    button = KEY_1\n    config = KEY_1\n    prog = pysoc\nend\nbegin\n    button = KEY_2\n    config = KEY_2\n    prog = pysoc\nend\nbegin\n    button = KEY_3\n    config = KEY_3\n    prog = pysoc\nend" > /etc/lirc/lircrc' &&
# Restart `lirc` service.
sudo /etc/init.d/lirc stop &&
sudo /etc/init.d/lirc start