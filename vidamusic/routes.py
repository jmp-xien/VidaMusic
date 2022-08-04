# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

import os, time, re
from passlib.hash import bcrypt
from flask import request, flash, url_for, escape, current_app, \
    redirect, render_template, session, send_from_directory, send_file
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


class Video_Proc:
    def __init__(self, links, viddir, auddir):
        self.links  = links
        self.viddir = viddir
        self.auddir = auddir
        self.video_title_list = []
        self.audio_title_list = []

    def download_vid(self):
        print("Dowloading listed videos...")
        cleanli = self.links.strip()
        linklst = re.split(r'[\n\r\t\f\v ]+', cleanli)
        print('Link list:', linklst)
        for li in linklst:
            vt = proc_download_vid(li, self.viddir)
            self.video_title_list.append(vt)
        return True

    def extract_audio(self):
        # loop titles
        print("Converting video to mp3 music file")
        for vft in self.video_title_list:
            print("Extracting audio from:", vft)
            at = proc_convert_mp3(vft, self.auddir, self.viddir)
            self.audio_title_list.append(at)
        print("Completed conversion to mp3 audio")
        return self.audio_title_list


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
            return redirect(url_for('index'))
        if not (auddir.strip() or caudd):
            flash(f'ERROR: An invalid Audio directory was Provided', 'error')
            return redirect(url_for('index'))

        vp  = Video_Proc(links, viddir, auddir)
        vd  = vp.download_vid()
        afl = vp.extract_audio()

        if afl:
            flash(f'INFO: Converted videos to mp3 music files', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return render_template("process.html", audiolist=afl, username=username, auddir=auddir)
    return render_template("index.html", form=form, pageid=pageid, pageli=pageli, username=username)


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


@app.route("/guest", methods=['GET', 'POST'])
def guest():
    auth = True
    if auth:
        session["username"] = 'guest'
    return redirect(url_for('index'))


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


@app.route('/download/<auddir>/<path:filename>', methods=['GET', 'POST'])
def download(auddir, filename):
    if "username" in session:
        username = escape(session["username"])
    else:
        return redirect(url_for('login'))
    root_dir = '/home/manny/Share/VidaMusic'
    basepath = root_dir + '/' + auddir + '/'
    path = basepath + filename
    # return send_from_directory(dirpath, filename, as_attachment=True)
    return send_file(path, as_attachment=True)


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('INFO: You are now Logged-Out.', 'error')
    return redirect(url_for('login'))


@app.route("/useredit", methods=['GET', 'POST'])
def useredit():
    username = 'guest'
    pageid = "intro"
    pageli = page[pageid]
    users = User.query.all()
    form = UserUpdate(request.form)
    return render_template("useredit.html",
        pageid=pageid, pageli=pageli, form=form,
        username=username, users=users)

