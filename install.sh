#!/bin/env bash

tar -xf VidaMusic.tar

pip3 install --no-input flask flask_wtf wtforms pytube

cd ./VidaMusic/

python3 run.py


