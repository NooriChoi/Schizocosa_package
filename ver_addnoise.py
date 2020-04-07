# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 19:24:14 2020

1. Add noise to laboratory recordings
from https://timsainburg.com/noise-reduction-python.html

@author: Noori Choi
"""

from scipy.io import wavfile
import numpy as np
import os
from pathlib import Path

# Working directory
wd = "D:/Lab/PhD thesis/Python/dup"
root_path = Path(wd)
sounds = os.listdir(wd)
# Directory where to save the csv file, must be different with wd
filt_loc = "D:/Lab/PhD thesis/Python/2_noise"

def fftnoise(f):
    f = np.array(f, dtype="complex")
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1 : Np + 1] *= phases
    f[-1 : -1 - Np : -1] = np.conj(f[1 : Np + 1])
    return np.fft.ifft(f).real


def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1 / samplerate))
    f = np.zeros(samples)
    f[np.logical_and(freqs >= min_freq, freqs <= max_freq)] = 1
    return fftnoise(f)

for s in sounds:
    print("processing " + s)
    rate, data = wavfile.read(wd + '/' + s)
    data = data / 32768
    
    noise_len = 2 # seconds
    noise = band_limited_noise(min_freq=100, max_freq = 700, samples=len(data), samplerate=rate)*10
    noise_clip = noise[:rate*noise_len]
    
    audio_noise = data + noise
    wavfile.write(filt_loc + '/' + s[:-4] + "_n.wav", rate, audio_noise)

