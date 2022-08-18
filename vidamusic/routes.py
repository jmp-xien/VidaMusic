# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms, flask_sqlalchemy

import os, re, ssl, ast
from secure_smtplib import smtplib
from datetime import datetime
from passlib.hash import bcrypt
from flask import request, flash, url_for, escape, current_app, \
    redirect, render_template, session, send_from_directory, send_file
from vidamusic import app, db
from vidamusic.models import User
from vidamusic.forms import VideoList, LoginForm, UserAdd, UserUpdate, \
        PwdReset
from vidamusic.process import proc_download_vid, proc_convert_mp3, \
        proc_check_dir, read_infile, proc_create_dir

page = {
    "intro": "Main Page",
    "login": "Log-In",
    "reset": "Reset Password",
    "newacc": "Add User",
    "audconv": "Convert Audio",
    "vidconv": "Video Download",
    "profile": "Edit Account",
    "download": "Download Video",
    "progress": "Converting",
    "pwdreset": "Reset Password",
    "useredit": "Edit User",
    "useradmin": "User Admin",
}

class User_Proc:
    def __init__(self, username=None):
        self.username = username

    def get_uid(self, username):
        user = User.query.filter_by(username=username).first()
        return user.id

    def check_email(self, email):
        chkeml = User.query.filter_by(email=email).first()
        if chkeml:
            return True
        return False

    def check_username(self, username):
        chkusr = User.query.filter_by(username=username).first()
        if chkusr:
            return True
        return False

    def add_user(self, form):
        username = form.username.data.strip()
        password = form.password.data.strip()
        email  = form.email.data.strip()
        chkusr = self.check_username(username)
        chkeml = self.check_email(email)
        if chkusr:
            flash(f'ERROR: Username already exists', 'error')
            return False
        if chkeml:
            flash(f'ERROR: Username with provide email already exists', 'error')
            return False
        admin  =  'No'
        pwhash =  bcrypt.hash(password)
        newuser = User(username, pwhash, email, admin)
        db.session.add(newuser)
        db.session.commit()
        return True

    def update_user(self, form, updpw):
        user = User.query.get(form.uid.data)
        user.username = form.username.data.strip()
        user.email =  form.email.data.strip()
        password  = form.password.data.strip()
        if updpw:
            pwhash =  bcrypt.hash(password)
            user.password = pwhash
        db.session.commit()
        return True

    def auth_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user:
            # InPw,DBhash: bcrypt.verify(in-pw, db-hash)
            pwd_match = bcrypt.verify(password, user.password)
            if pwd_match:
                return True
            else:
                return False
        return False

    def reset_account(self, form):
        username = form.username.data.strip()
        email = form.email.data.strip()
        user = User.query.filter_by(username=username).first()
        if user:
            if not user.email == email:
                flash(f'ERROR: "Email does not match the account username', 'error')
                return False
        else:
            flash(f'ERROR: "Provided account username was not found', 'error')
            return False
        eml = user.email
        uid = user.id
        upw = user.password
        now = datetime.now()
        tms = now.strftime("%H%M%S")
        hst = request.host
        rli = '/pwdreset/p/reset?prurl=' + str(uid) + str(tms) + str(upw)
        print("Reset link: ", rli)
        emlcrd = {}
        filena = 'vidamusic.conf'
        fipath = '/opt/secure/conf'
        tmpcrd = read_infile(filena, fipath)
        emlcrd = ast.literal_eval(tmpcrd)
        sender = emlcrd['euname'] + '@' + emlcrd['domain']
        receiver = eml
        emailacc = emlcrd['euname'] + '@' + emlcrd['domain']
        password = emlcrd['passwd']
        smtpserv = emlcrd['smtp']
        port = 465
        msg1 = f"from: {sender}\nto: {receiver}\nsubject: Password Reset\n\n\n"
        msg2 = f"Hello,\n\nReset your password to VidaMusic.com\nLink: https://www.google.com{rli}\n\n"
        msg3 = "VidaMusic"
        message = msg1+msg2+msg3
        context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(smtpserv, port, context=context, timeout=30) as server:
        #     server.login(emailacc, password)
        #     server.sendmail(sender, receiver, message)
        flash('NOTE: Link to reset account was sent to your email', 'info')
        return True

    def del_user(self, inuid):
        uid = int(inuid)
        user = User.query.get(uid)
        if uid == 1 or user.id == 1 or user.username == "admin":
            flash('ERROR: Unable to delete Admin account', 'error')
            return False
        print("Deleting query for user:", user)
        db.session.delete(user)
        db.session.commit()
        return True


class Video_Proc:
    def __init__(self, links, viddir, auddir):
        self.links  = links
        self.viddir = proc_create_dir(viddir)
        self.auddir = proc_create_dir(auddir)
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
        # Loop every video title
        print("Converting video to mp3 music file")
        for vft in self.video_title_list:
            print("Extracting audio from:", vft)
            at = proc_convert_mp3(vft, self.auddir, self.viddir)
            self.audio_title_list.append(at)
        print("Completed conversion of video to mp3 audio")
        return self.audio_title_list


# Begin Video processing routes
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
        viddir = form.dirvid.data.strip()
        auddir = form.diraud.data.strip()
        cvidd = proc_check_dir(viddir)
        caudd = proc_check_dir(auddir)

        if not (viddir or cvidd):
            flash(f'ERROR: An invalid Video directory was Provided', 'error')
            return redirect(url_for('index'))
        if not (auddir or caudd):
            flash(f'ERROR: An invalid Audio directory was Provided', 'error')
            return redirect(url_for('index'))
        vp  = Video_Proc(links, viddir, auddir)
        vd  = vp.download_vid()
        afl = vp.extract_audio()
        if afl:
            flash(f'INFO: Converted videos to mp3 music files', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return render_template("process.html", audiolist=afl, username=username, auddir=vp.auddir)
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
        up = User_Proc()
        nu = up.add_user(form)
        if nu:
            flash(f'INFO: Added new user account to VidaMusic site', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'ERROR: Unable to create new account', 'error')
    return render_template("newacc.html", form=form, pageid=pageid, pageli=pageli, username=username)


@app.route('/download/<auddir>/<path:filename>', methods=['GET', 'POST'])
def download(auddir, filename):
    if "username" in session:
        username = escape(session["username"])
    else:
        return redirect(url_for('login'))
    # change DIR to be a secure location 
    root_dir = '/opt/secure/web/VidaMusic'
    basedir = root_dir + '/' + auddir + '/'
    path = basedir + filename
    # return send_from_directory(dirpath, filename, as_attachment=True)
    return send_file(path, as_attachment=True)


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('INFO: You are now Logged-Out.', 'error')
    return redirect(url_for('login'))


# Admin Access: user edit
@app.route("/useradmin", methods=['GET', 'POST'])
def useradmin():
    if "username" in session:
        username = escape(session["username"])
    else:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    if not user.admin == "Yes":
        flash(f'ERROR: Access not allowed. Must be admin to edit users', 'error')
        return redirect(url_for('index'))
    pageid = "useradmin"
    pageli = page[pageid]
    users = User.query.all()
    form = UserUpdate(request.form)
    if request.method == 'POST':
        password = form.password.data.strip()
        confpw = form.password_confirm.data.strip()
        updpw  = False
        if not (password == '' or password == None):
            if not password == confpw:
                flash(f'ERROR: Passwords do not match, please retry', 'error')
                return redirect(url_for('useredit'))
            else:
                updpw = True
        up = User_Proc()
        uu = up.update_user(form, updpw)
        if uu:
            flash(f'INFO: Updated user account in VidaMusic site', 'success')
        else:
            flash(f'ERROR: Failed to update user information', 'error')
    return render_template("useredit.html", pageid=pageid, pageli=pageli,
            form=form, username=username, users=users)


# Admin Access: delete accounts
@app.route("/delacc/<uid>/<proc_uname>", methods=['GET', 'POST'])
def delacc(uid, proc_uname):
    if "username" in session:
        username = escape(session["username"])
    else:
        return redirect(url_for('login'))
    # No POST
    # Check logged in user is admin
    user = User.query.filter_by(username=username).first()
    if not user.admin == "Yes":
        flash(f'ERROR: Must be admin to delete user { proc_uname }', 'error')
        return redirect(url_for('useredit'))
    if uid == 1 or uid == "1":
        flash(f'ERROR: Deleting main Admin account is not allowed', 'error')
        return redirect(url_for('useredit'))
    up = User_Proc()
    du = up.del_user(uid)
    if du:
        flash(f'INFO: Account {proc_uname} is now deleted in VidaMusic', 'error')
    else:
        flash(f'ERROR: Deleting user {proc_uname} failed', 'error')
    return redirect(url_for('useredit'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if "username" in session:
        username = escape(session["username"])
    else:
        return redirect(url_for('login'))
    usr_dt = []
    pageid = "profile"
    pageli = page[pageid]
    proc_user = User.query.filter_by(username=username).first()
    if not proc_user or username == 'guest':
        flash(f'ERROR: Unable to edit "guest" profiles', 'error')
        return redirect(url_for('index'))
    form = UserUpdate(request.form)
    usr_dt.append(proc_user)
    if request.method == 'POST':
        if not username == proc_uname:
            flash(f'ERROR: Unable to load your profile due to error', 'error')
            return redirect(url_for('index'))
        password = form.password.data.strip()
        confpw = form.password_confirm.data.strip()
        updpw  = False
        if not (password == '' or password == None):
            if not password == confpw:
                flash(f'ERROR: Passwords do not match', 'error')
                return redirect(url_for('profile'))
            else:
                updpw = True
        up = User_Proc()
        uu = up.update_user(form, updpw)
        if uu:
            flash(f'INFO: Updated your user account in VidaMusic', 'success')
        else:
            flash(f'ERROR: Updating your information failed', 'error')
    return render_template("profile.html", pageid=pageid, pageli=pageli,
            form=form, username=username, usr=usr_dt)


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    pageid = "reset"
    pageli = page[pageid]
    form = PwdReset(request.form)
    if request.method == 'POST':
        up = User_Proc()
        ra = up.reset_account(form)
        if ra:
            return redirect(url_for('login'))
    return render_template("reset.html", form=form, pageid=pageid, pageli=pageli)


@app.route("/pwdreset/p/reset", methods=['GET', 'POST'])
def pwdreset():
    url_args = request.args
    full_url = url_args['prurl']
    uid_time, pw_url = full_url.split('$', 1)
    in_pwd = '$' + str(pw_url)
    tms = uid_time[-6:]
    uid = uid_time[:-6]
    pageid = "pwdreset"
    pageli = page[pageid]
    u = User.query.get(uid)
    if not u.password == in_pwd:
        flash(f'ERROR: Unable to reset user or invalid link', 'error')
        return redirect(url_for('reset'))
    else:
        print("Resetting user password.")
    form = UserUpdate(request.form)
    usr_dt = []
    usr_dt.append(u)
    if request.method == 'POST':
        password = form.password.data.strip()
        confpw = form.password_confirm.data.strip()
        updpw  = True
        if not (password == '' or password == None):
            if not password == confpw:
                flash(f'ERROR: Passwords do not match', 'error')
            return render_template("pwdreset.html", pageid=pageid, pageli=pageli,
                form=form, username='#', usr=usr_dt)
        up = User_Proc()
        uu = up.update_user(form, updpw)
        if uu:
            flash(f'INFO: Updated your user account in VidaMusic', 'success')
        else:
            flash(f'ERROR: Password reset failed, contac site admin.', 'error')
    return render_template("pwdreset.html", pageid=pageid, pageli=pageli,
            form=form, username='#', usr=usr_dt)
