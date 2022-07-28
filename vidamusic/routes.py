# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

import time, re
from passlib.hash import bcrypt
from flask import request, flash, url_for, escape, \
    redirect, render_template, session
from vidamusic import app, db
from vidamusic.models import User
from vidamusic.forms import VideoList, LoginForm, UserAdd, UserUpdate
from vidamusic.process import proc_download_vid, proc_convert_mp3, proc_check_dir

page = {
    "intro": "Main Page",
    "login": "Log-In",
    "newacc": "Add User",
    "progress": "Converting",
    "vidconv": "Convert Video",
    "audconv": "Convert Audio",
    "download": "Download Video",
}

class User_Proc:
    def __init__(self, username=None):
        self.username = username

    def get_uid(self, username):
        user = User.query.filter_by(username=username).first()
        return user.id

    def add_user(self, form):
        username = form.username.data.strip()
        password = form.password.data.strip()
        email  =  form.email.data.strip()
        admin  =  'No'
        pwhash =  bcrypt.hash(password)
        newuser = User(
            username,
            pwhash,
            email,
            admin,
        )
        db.session.add(newuser)
        db.session.commit()
        return True

    def auth_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user:
            # InPw,DBhash: bcrypt.verify(in-pw, db-hash)
            pw_match = bcrypt.verify(password, user.password)
            if pw_match:
                return True
            else:
                return False
        return False


class Link_Proc:
    def __init__(self, links, viddir, auddir):
        self.links   = links
        self.viddir = viddir
        self.auddir = auddir

    def download_vid(self):
        print("Dowloading listed videos...")
        print(f'Links: "{self.links}"')
        cleanli = self.links.strip()
        linklst = re.split(r'[\n\r\t\f\v ]+', cleanli)
        print('CleanLinks:', linklst)
        for li in linklst:
            proc_download_vid(li, self.viddir)
        return True

    def convert_aud(self):
        print("Converting videos to mp3 music...")
        audlist = proc_convert_mp3(self.auddir, self.viddir)
        return audlist


# Begin Video processing pages
@app.route("/", methods=['GET', 'POST'])
def index():
    if "username" in session:
        username = escape(session["username"])
    else:
        return redirect(url_for('login'))

    pageid = "intro"
    pageli = page[pageid]
    form = VideoList(request.form)

    if request.method == 'POST':
        links  = form.videolink.data
        viddir = form.dirvid.data
        auddir = form.diraud.data

        cvidd = proc_check_dir(viddir)
        caudd = proc_check_dir(auddir)
        if not (viddir.strip() or cvidd):
            flash(f'ERROR: An invalid Video directory was Provided', 'error')
            return render_template("index.html", form=form, pageid=pageid, pageli=pageli, username=username)
        if not (auddir.strip() or caudd):
            flash(f'ERROR: An invalid Audio directory was Provided', 'error')
            return render_template("index.html", form=form, pageid=pageid, pageli=pageli, username=username)

        pv = Link_Proc(links, viddir, auddir)
        vd = pv.download_vid()
        ac = pv.convert_aud()
        if ac:
            flash(f'INFO: Converted videos to mp3 music files', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return render_template("process.html", audio_li=ac)
    return render_template("index.html", form=form, pageid=pageid, pageli=pageli, username=username)


@app.route("/guest", methods=['GET', 'POST'])
def guest():
    if "username" in session:
        username = escape(session["username"])
    else:
        username = 'guest'

    pageid = "intro"
    pageli = page[pageid]
    form = VideoList(request.form)

    if request.method == 'POST':
        links  = form.videolink.data
        viddir = form.dirvid.data
        auddir = form.diraud.data

        cvidd = proc_check_dir(viddir)
        caudd = proc_check_dir(auddir)
        if not (viddir.strip() or cvidd):
            flash(f'ERROR: An invalid Video directory was Provided', 'error')
            return render_template("progress.html", form=form, pageid=pageid, pageli=pageli, username=username)
        if not (auddir.strip() or caudd):
            flash(f'ERROR: An invalid Audio directory was Provided', 'error')
            return render_template("progress.html", form=form, pageid=pageid, pageli=pageli, username=username)

        pv = Link_Proc(links, viddir, auddir)
        vd = pv.download_vid()
        ac = pv.convert_aud()
        # ac = ['First Music Video File.mp3','Second Music Video File.mp3']
        time.sleep(15)
        if ac:
            flash(f'INFO: Converted video to mp3 music files', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return render_template("process.html", audio_li=ac)
    return render_template("progress.html", form=form, pageid=pageid, pageli=pageli, username=username)


@app.route("/process")
def process():
    if "username" in session:
        username = escape(session["username"])
    else:
        return redirect(url_for('login'))
    pageid = "vidconv"
    pageli = page[pageid]
    ac = False
    if ac:
        flash(f'INFO: Converted video files to mp3 music', 'success')
    else:
        flash(f'ERROR: Video file conversion to mp3 failed', 'error')
    return render_template("process.html", audio_li=ac, username=username)


@app.route("/login", methods=['GET', 'POST'])
def login():
    pageid = "login"
    pageli = page[pageid]
    form = LoginForm(request.form)

    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        ua = User_Proc()
        auth = ua.auth_user(username, password)
        if auth:
            session["username"] = username
            return redirect(url_for('index'))
        else:
            flash('ERROR: Invalid username or password', 'error')
    return render_template("login.html", form=form, pageid=pageid, pageli=pageli)


@app.route("/newacc", methods=['GET', 'POST'])
def newacc():
    if "username" in session:
        username = escape(session["username"])
    else:
        username = 'guest'

    pageid = "newacc"
    pageli = page[pageid]
    form = UserAdd(request.form)
    if request.method == 'POST':
        au = User_Proc()
        nu = au.add_user(form)
        if nu:
            flash(f'INFO: Added new user account to VidaMusic site', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'ERROR: Adding new user failed', 'error')
    return render_template("newacc.html", form=form, pageid=pageid, pageli=pageli, username=username)


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('INFO: You are now Logged-Out.', 'error')
    return redirect(url_for('login'))


@app.route("/modal1")
def modal1():
    pageid = "intro"
    pageli = page[pageid]
    return render_template("modal1.html", pageid=pageid, pageli=pageli)

