#!/bin/bash
pyinstaller --paths="./src" --paths="./src/cli" --paths="./src/collection-function" --paths="./src/config-and-database" --paths="./src/input" --onefile pysoc.py
$SHELL