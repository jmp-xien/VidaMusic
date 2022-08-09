# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectField, \
     FileField, TextAreaField, HiddenField, validators, RadioField
from wtforms.validators import ValidationError, DataRequired

kwph='placeholder'
kw0={kwph: 'Input Links'}
kw1={kwph: 'Video Directory'}
kw2={kwph: 'Audio Directory'}
kw3={kwph: 'Email'}
kw4={kwph: 'Username'}
kw5={kwph: 'Password'}
kw6={kwph: 'Verify Password'}
kw7={kwph: 'Is Admin'}

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


class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()],
        render_kw=kw4)
    password = PasswordField(u'Password', validators=[DataRequired()],
        render_kw=kw5)
    submit = SubmitField(label=('Log-In'))


class BaseUser(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()],
        render_kw=kw4)
    email = StringField(u'Email', validators=[DataRequired()],
        render_kw=kw3)
    admin = RadioField('Admin User', validators=[DataRequired()],
        choices=[('No', 'No'), ('Yes', 'Yes')], default='No')


class UserAdd(BaseUser):
    password = PasswordField(u'Password', validators=[
        validators.Length(min=8, max=24),
        validators.EqualTo('password_confirm',
        message='Passwords do not match')], render_kw=kw5)
    password_confirm = PasswordField(u'Password Confirm', 
        validators=[validators.Length(min=8, max=24)], render_kw=kw6)
    submit = SubmitField(label=('Add User'))


class UserUpdate(BaseUser):
    uid = HiddenField('uid', validators=[DataRequired()])
    password = PasswordField(u'Password', render_kw=kw5)
    password_confirm = PasswordField(u'Confirm Password', render_kw=kw6)
    admin = SelectField('Admin User', choices=None,
        validators=[DataRequired()])
    submit = SubmitField(label=('Update'))


class ResetAcc(BaseUser):
    username = StringField(u'Username', validators=[DataRequired()],
        render_kw=kw4)
    email = StringField(u'Email', validators=[DataRequired()],
        render_kw=kw3)
    submit = SubmitField(label=('Reset Account'))