#!/bin/sh

BIN="src/bin"
SRC="src/main.py"

python3 -m venv env
source "env/bin/activate"
pip install -r "src/requirements.txt"
python3 "$SRC" -b "$BIN" "$*" && deactivate
