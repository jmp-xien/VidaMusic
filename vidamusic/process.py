# Converts FLV, MP4, WMV, and WEBM videos' audio into MP3 music files
# Program written by:
# Author:   J. Manuel Perez
# Date:     01/01/2020
# Version:  0.01

import os, time, subprocess
from pytube import YouTube 

del_chars = [';', ':', ",", "'"]

def proc_download_vid(link, vidpath):
    yt = YouTube(link) 
    vt = yt.title.title()
    for ch in del_chars:
        vt = vt.replace(ch, '')
    print(f"Processing video file: {vt}.mp4")
    vidfp = vidpath + '/' + vt + '.mp4'
    print(f"Checking if file exists: {vidfp}")
    videx = os.path.exists(vidfp)
    if videx:
        print("Video file exists in directory!")
        return False
    else:
        print("Downloading new video file")
        yt.streams.get_highest_resolution()
        yt.streams.get_audio_only().download(vidpath)
    print(f'Download complete: {vt}') 
    return True


def proc_convert_mp3(audpath, vidpath):
    flist = os.listdir(audpath)
    for f in flist:
        print(f"Converting video to music: {f}")   
        vnn = f
        # REMOVE INVAL CHAR
        for ch in del_chars:
            vnn = vnn.replace(ch, '')
        vnfp = vidpath + '/' + vnn
        vofp = vidpath + '/' + f
        vnfx = os.path.exists(vnfp)
        if not vnfx:
            print("Renaming video file")
            cmd1 = 'mv "' + vofp + '" "' + vnfp + '"'
            subprocess.run(cmd1, shell=True)
        else:
            print("Keeping original file name")

        vidbn, _ = vnn.rsplit('.', 1)
        mp3fn = vidbn + '.mp3'
        audfp = audpath + '/' + mp3fn
        print("Full mp3 file path:", audfp)
        afex = os.path.exists(audfp)
        if afex:
            print("File already in mp3 format")
        else:
            print(f"Processing to mp3 audio: {mp3fn}")
            wavdump = "audiodump.wav"
            oscmd1 = 'vlc "' + vnfp + '" -I dummy --no-sout-video --sout \'#transcode{acodec=s16l,samplerate=44100}:std{mux=wav,access=file,dst=audiodump.wav}\' vlc://quit'
            oscmd2 = 'lame -h -b 192 ' + wavdump + ' "' + audfp + '"'
            oscmd3 = 'rm ' + wavdump
            subprocess.run(oscmd1, shell=True)
            subprocess.run(oscmd2, shell=True)
            subprocess.run(oscmd3, shell=True)
    return True
    
