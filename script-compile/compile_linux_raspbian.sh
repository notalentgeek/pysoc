#!/bin/bash
sudo pyinstaller --paths="./src/cli" --paths="./src/collection-function" --paths="./src/config-and-database" --paths="./src/input" --paths="./src/other" --onefile pysoc.py
$SHELL