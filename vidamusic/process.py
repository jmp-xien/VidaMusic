# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

import os, time, subprocess, re
from pytube import YouTube

del_chars = ['.', ';' ':', ",", "'"]

def proc_download_vid(link, vidpath):
    yt = YouTube(link)
    vt = yt.title.title()
    vf = yt.streams.get_highest_resolution().default_filename
    # vf rename(yt.streams.first().default_filename, 'new_fname.ext')
    print(f"Processing video file: {vt}")
    vidti = vidpath + '/' + vt + '.mp4'
    vidfn = vidpath + '/' + vf
    print(f"Checking if file exists, full path: {vf}")
    vttex = os.path.exists(vidti)
    vfnex = os.path.exists(vidfn)
    if vfnex or vttex:
        print("Video file exists in directory")
        return vf
    else:
        print("Downloading new video file")
        yt.streams.get_highest_resolution()
        yt.streams.get_audio_only().download(vidpath)
    print(f'Download complete: {vt}')
    return vf


def proc_convert_mp3(vft, audpath, vidpath):
    vidfp = vidpath + '/' + vft
    print("Checkinf for file: ", vidfp)
    vnfx = os.path.exists(vidfp)
    if not vnfx:
        print("Invalid video file name or path")
        return None
    vidbn, _ = vft.rsplit('.', 1)
    mp3fn = vidbn + '.mp3'
    print('MP3 file name: ', mp3fn)
    audfp = audpath + '/' + mp3fn
    afex = os.path.exists(audfp)
    if afex:
        print("Video file already in mp3 format")
    else:
        print(f"Converting audio to mp3 format: {mp3fn}")
        wavdump = "audiodump.wav"
        oscmd1 = 'vlc "' + vidfp + '" -I dummy --no-sout-video --sout \'#transcode{acodec=s16l,samplerate=44100}:std{mux=wav,access=file,dst=audiodump.wav}\' vlc://quit'
        oscmd2 = 'lame -h -b 192 ' + wavdump + ' "' + audfp + '"'
        oscmd3 = 'rm ' + wavdump
        subprocess.run(oscmd1, shell=True)
        subprocess.run(oscmd2, shell=True)
        subprocess.run(oscmd3, shell=True)
    return mp3fn


def proc_check_dir(dirname):
    valchr = re.compile(r"[-_A-Za-z0-9]")
    if not valchr.search(dirname):
        return False
    else:
        return True