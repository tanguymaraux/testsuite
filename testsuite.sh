#!/bin/sh

BIN="template/program.sh" # path to your program to test
SRC="src/main.py" # path to the testsuite

pip install -r "src/requirements.txt" # install requirements

# run testsuite
python3 "$SRC" -b "$BIN" "$@" # insert testsuite argument (ie: '-p template')
