#!/bin/bash
pyinstaller --paths="/home/pi/pysoc/src" --paths="/home/pi/pysoc/src/cli" --paths="/home/pi/pysoc/src/collection-function" --paths="/home/pi/pysoc/src/config-and-database" --paths="/home/pi/pysoc/src/input" --onefile /home/pi/pysoc/pysoc.py
$SHELL