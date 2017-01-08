#!/bin/bash
pyinstaller --paths="./src/cli" --paths="./src/collection_function" --paths="./src/config_and_database" --paths="./src/input" --paths="./src/other" --onefile pysoc.py
$SHELL