#!/bin/env bash

# Create python virtual env
/bin/python3.10 -m venv ~/venv/vidapy

source ~/venv/vidapy/bin/activate

pip3 ~/venv/vidapy/bin/pip install --no-input flask flask_wtf flaks_sqlalchemy sqlalchemy wtforms secure_smtplib pytube

tar -xf VidaMusic.tar

cd ./VidaMusic/

echo "VidaMusic installed and running with below indicated options:"
echo ''

python3 run.py

