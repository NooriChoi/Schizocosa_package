# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 21:10:34 2020

1. code from "https://m.blog.naver.com/PostList.nhn?blogId=aimldl"

@author: aimldl
"""
import wave
import os
from pathlib import Path
import subprocess

wd = "D:/Lab/PhD thesis/Python/test"
root_path = Path(wd)
sounds = os.listdir(wd)
filt_loc = "D:/Lab/PhD thesis/Python/test_result"

def pcm2wav(pcm_file, wav_file):
    # Read the .pcm file as a binary file and store the data to pcm_data
    with open(pcm_file, 'rb') as opened_pcm_file:
        pcm_data = opened_pcm_file.read();
    
    with wave.open(wav_file, 'wb') as wavfile:
        wavfile.setparams((1, 2, 48000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcm_data)

for s in sounds:
    print("Processing " + s)
    pcm2wav(wd + '/' + s, filt_loc + '/' + s[:-4] + '3.wav')
    