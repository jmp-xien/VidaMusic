# Converts FLV, MP4, WMV, and WEBM videos' audio into MP3 music files
# Program written by:
# Author:   J. Manuel Perez
# Date:     01/01/2020
# Version:  0.01

import time, re
from flask import request, flash, url_for, \
    redirect, render_template
from vidamusic import app
from vidamusic.forms import VideoList
from vidamusic.process import proc_download_vid, proc_convert_mp3

page = {
    "intro": "Main Page",
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
        pv = Proc_Links(links, viddir, auddir)
        vd = pv.download_vid()
        ac = pv.convert_aud()
        ## ac = ['First File Name1.mp3','File Name Long Other2.mp3']
        if ac:
            flash(f'INFO: Converted video files to mp3 music', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return render_template("process.html", audio_li=ac)
    return render_template("index.html", form=form, pageid=pageid, pageli=pageli)


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


@app.route("/home")
def home():
    pageid="intro"
    pageli=page[pageid]
    return render_template("home.html", pageid=pageid, pageli=pageli)

