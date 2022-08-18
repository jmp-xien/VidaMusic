# Extracts and converts audio from FLV, MP4, WMV, and WEBM video files into MP3 music files
# Python Web Application Program:
# Author:   J. Manuel Perez
# License:  Mozilla Public License Version 2.0
# Date:     01/01/2020
# Version:  0.01
# Requires:
#  flask, pytube, flask_wtf, wtforms

import os, subprocess, re, random, string
from pytube import YouTube

del_chars = [';' ':', ",", "'"]

def proc_download_vid(link, vidpath):
    yt = YouTube(link)
    vt = yt.title.title()
    vf = yt.streams.get_highest_resolution().default_filename
    # vf rename(yt.streams.first().default_filename, 'new_fname.ext')
    print(f"Processing video file: {vt}")
    vidti = vidpath + '/' + vt + '.mp4'
    vidfn = vidpath + '/' + vf
    print(f"Checking if file exists: {vf}")
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
    print("Checking if file downloaded: ", vidfp)
    vnfx = os.path.exists(vidfp)
    if not vnfx:
        print("Invalid video file name or path")
        return None
    vidbn, _ = vft.rsplit('.', 1)
    mp3fn = vidbn + '.mp3'
    print('Cheking for MP3 file name: ', mp3fn)
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
    valchr = re.compile(r"^[A-Za-z][-_A-Za-z0-9]{:23}")
    if not valchr.search(dirname):
        return False
    else:
        return True


def proc_gen_id(idlen):
    r_alnu = string.ascii_lowercase + string.ascii_uppercase + string.digits
    newid = ''.join(random.SystemRandom().choice(r_alnu) for _ in range(idlen))
    return newid


def proc_create_dir(dirname): 
    dina_le = 6  
    dirsuff = proc_gen_id(dina_le)
    newdir = dirname + "_" + dirsuff
    cmd1 = 'mkdir ' + newdir
    subprocess.run(cmd1, shell=True)
    return newdir
    

def read_infile(filename, path):
    indict = None
    fullfp = path + '/' + filename
    with open(fullfp, 'r') as infi:
        indict = infi.readline()
    return indict

