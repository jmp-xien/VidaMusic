# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

from sqlalchemy import Integer, String, Column
from datetime import datetime
from vidamusic import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    admin = db.Column(db.String(8), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User(id='{self.id}', username='{self.username}', password='{self.password}', email='{self.email}', admin='{self.admin}')"

    def __init__(self, username, password, email, admin):
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin
