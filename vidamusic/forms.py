# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, \
     FileField, TextAreaField, HiddenField, validators
from wtforms.validators import ValidationError, DataRequired

kwph='placeholder'
kw0={kwph: 'Input Links'}
kw1={kwph: 'Video Directory'}
kw2={kwph: 'Audio Directory'}
kw3={kwph: 'Email'}
kw4={kwph: 'Host Name'}
kw5={kwph: 'IP Address'}
kw6={kwph: 'Service'}

dirlist = [('windows', "C:/users/username/Music : enter username"), \
        ('linux', "/home/username/Music : enter username")]

class VideoList(FlaskForm):
    # sid = HiddenField('uid', validators=[DataRequired()])
    videolink = TextAreaField(u'Video Links', validators=[DataRequired()],
        render_kw=kw0)
    dirvid = StringField(u'Video Dir', validators=[DataRequired()],
        render_kw=kw1)
    diraud = StringField(u'Audio Dir', validators=[DataRequired()],
        render_kw=kw2)
    submit = SubmitField(label=('Convert To Audio'))
