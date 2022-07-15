# Converts FLV, MP4, WMV, and WEBM videos' audio into MP3 music files
# Program written by:
# Author:   J. Manuel Perez
# Date:     01/01/2020
# Version:  0.01

import time
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
        linkli = self.links.split(' ')
        for li in linkli:
            vd = proc_download_vid(li, self.viddir)
        return True

    def convert_aud(self):
        print("Converting videos to mp3 music...")
        vc = proc_convert_mp3(self.auddir, self.viddir)
        return True


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
        vc = pv.convert_aud()
        if vc:
            flash(f'INFO: Converted video files to mp3 music', 'success')
        else:
            flash(f'ERROR: Video file conversion to mp3 failed', 'error')
        return redirect(url_for('convert'))
    return render_template("index.html", form=form, pageid=pageid, pageli=pageli)


@app.route("/convert")
def convert():
    pageid="intro"
    pageli=page[pageid]
    return render_template("convert.html", pageid=pageid, pageli=pageli)


@app.route("/home")
def home():
    pageid="intro"
    pageli=page[pageid]
    return render_template("home.html", pageid=pageid, pageli=pageli)

