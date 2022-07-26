# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

import time, re
from flask import request, flash, url_for, \
    redirect, render_template
from vidamusic import app
from vidamusic.forms import VideoList
from vidamusic.process import proc_download_vid, proc_convert_mp3, proc_check_dir

page = {
    "intro": "Main Page",
    "login": "Log-In",
    "progress": "Converting",
    "vidconv": "Convert Video",
    "audconv": "Convert Audio",
    "download": "Download Video",
}

class Proc_Links:
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
    form = VideoList(request.form)
    pageid="intro"
    pageli=page[pageid]

    if request.method == 'POST':
        links  = form.videolink.data
        viddir = form.dirvid.data
        auddir = form.diraud.data

        cvidd = proc_check_dir(viddir)
        caudd = proc_check_dir(auddir)   
        if not (viddir.strip() or cvidd):
            flash(f'ERROR: An invalid Video directory was Provided', 'error')
            return render_template("index.html", form=form, pageid=pageid, pageli=pageli)
        if not (auddir.strip() or caudd):
            flash(f'ERROR: An invalid Audio directory was Provided', 'error')
            return render_template("index.html", form=form, pageid=pageid, pageli=pageli)

        pv = Proc_Links(links, viddir, auddir)
        vd = pv.download_vid()
        ac = pv.convert_aud()
        if ac:
            flash(f'INFO: Converted video files to mp3 music', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return render_template("process.html", audio_li=ac)
    return render_template("index.html", form=form, pageid=pageid, pageli=pageli)


@app.route("/progress", methods=['GET', 'POST'])
def progress():
    form = VideoList(request.form)
    pageid="intro"
    pageli=page[pageid]

    if request.method == 'POST':
        links  = form.videolink.data
        viddir = form.dirvid.data
        auddir = form.diraud.data

        cvidd = proc_check_dir(viddir)
        caudd = proc_check_dir(auddir)   
        if not (viddir.strip() or cvidd):
            flash(f'ERROR: An invalid Video directory was Provided', 'error')
            return render_template("progress.html", form=form, pageid=pageid, pageli=pageli)
        if not (auddir.strip() or caudd):
            flash(f'ERROR: An invalid Audio directory was Provided', 'error')
            return render_template("progress.html", form=form, pageid=pageid, pageli=pageli)

        pv = Proc_Links(links, viddir, auddir)
        # vd = pv.download_vid()
        # ac = pv.convert_aud()
        ac = ['First File Name1.mp3','File Name Long Other2.mp3']
        time.sleep(15)
        if ac:
            flash(f'INFO: Converted video files to mp3 music', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return render_template("process.html", audio_li=ac)
    return render_template("progress.html", form=form, pageid=pageid, pageli=pageli)


@app.route("/process")
def process():
    pageid="vidconv"
    pageli=page[pageid]
    ac = False
    if ac:
        flash(f'INFO: Converted video files to mp3 music', 'success')
    else:
        flash(f'ERROR: Video file conversion to mp3 failed', 'error')
    return render_template("process.html", audio_li=ac)


@app.route("/login")
def login():
    pageid="login"
    pageli=page[pageid]
    return render_template("login.html", pageid=pageid, pageli=pageli)


@app.route("/modal1")
def modal1():
    pageid="intro"
    pageli=page[pageid]
    return render_template("modal1.html", pageid=pageid, pageli=pageli)

