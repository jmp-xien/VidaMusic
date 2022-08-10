#!/bin/env bash

pip3 install --no-input flask flask_wtf flaks_sqlalchemy sqlalchemy wtforms secure_smtplib pytube

tar -xf VidaMusic.tar

cd ./VidaMusic/

echo "VidaMusic installed and running as below with these options:"
echo ''

python3 run.py


