# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires: 
#  flask, pytube, flask_wtf, wtforms

from flask import Flask
from datetime import timedelta

# Setup TopDeck app environment 
app = Flask(__name__)
app.config['SECRET_KEY'] = "ztIx3p07gk6h9haf"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config['MAX_CONTENT_LENGTH'] = 4*1024*1024

from vidamusic import routes
