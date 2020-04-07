# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 00:28:00 2019

Third part of data analysis
1. Find chunks by peak finding
2. apply amp, freq filtering

@author: Noori Choi
"""
# Library imports
import os
import numpy as np
import pandas as pd
from scipy.signal import lfilter, hilbert, butter, find_peaks
import matplotlib
import soundfile as sf
from kneed import KneeLocator

matplotlib.use('Agg')
# Working directory
wd = "D:/Lab/PhD thesis/Python/test"
# Listof soundfiles
sounds = os.listdir(wd)
# Directory where to save the csv file, must be different with wd
csv_loc = "D:/Lab/PhD thesis/Python/4_peakfind"

# frequency for bandpass filter (in Hz)
lowcut = 200
highcut = 1000
#fs = 48000 # fs - sampling rate
dt = 0.03 # dt - time interval between peaks

def find_alpha(audio, lowest, highest, num):
    list_alpha = np.linspace(lowest, highest, num)
    
    audio_len = []
    for alpha in list_alpha:
        ab_audio = np.absolute(audio)
        A_low = np.median(ab_audio) + (alpha*np.std(ab_audio))
        #count number of samples below amp_threshold
        length = np.count_nonzero(audio > A_low)
        audio_len.append([alpha, length])
           
    audio_len = np.array(audio_len)    
    results = pd.DataFrame({'alpha': audio_len[:, 0], 'number': audio_len[:, 1]})
    
    kn = KneeLocator(results['alpha'], results['number'], curve='convex', direction='decreasing')
    
    if kn.knee:
        knee = kn.knee + ((highest-lowest)/num)
    else:
        knee = 0
        
    return knee

def peak_find(env):
    # sigma clipping for peak detection threshold
    A_low = np.median(env) + (alpha*np.std(env))
    peaks, properties = find_peaks(env, height = A_low, distance = dt*fs)
    time = np.ndarray.tolist(peaks/fs) # time of peaks in second
    amp = np.ndarray.tolist(properties["peak_heights"]) # amp of each peak
    peaks = np.column_stack((time, amp))
    return(peaks)    

def filt(block):
    f_NQ = fs / 2 # Nquist frequency
    b2, a2 = butter(5, [lowcut / f_NQ, highcut / f_NQ], "band")
    signal_filt = lfilter(b2, a2, block)  # bandpass filtering
    env = np.abs(hilbert(signal_filt)) #Envelope of the signal
    return(env)

def process(s, alpha):
    print("Analyzing the file " + s)
    # block processing
    env = np.concatenate([filt(block) for block in 
                          sf.blocks(wd + '/' + s, blocksize=fs*10)])
    #pool = Pool(processes = 5)
    #result = pool.map(filt, blocks)
    #env = sum(result)
    peaks = peak_find(env)
    # add file name as a separate column
    result = np.hstack((peaks, np.array([[s]] * len(peaks))))
    result
    # convert into dataframe
    df_res = pd.DataFrame({'Time': result[:, 0], 'Amp': result[:, 1], 'File': result[:,2]})
    return df_res

# for loop to go through every file
no_pulse = []
for s in sounds:
    data, fs = sf.read(wd + '/' + s)
    #get alpha for sigma clipping
    alpha = find_alpha(data, lowest=0, highest=3, num=10)
    
    if alpha > 0:
        # get result data (df_res)
        result_data = process(s, alpha)
        # Save as a csv file
        result_data.to_csv(csv_loc + '/' + s[:-4] + '.csv', index=False, sep = ",")
    else:
        print(s + " does not contain a pulse.")
        no_pulse.append(s)
        
print(no_pulse)
no_pulse_df = pd.DataFrame({'file':no_pulse})
no_pulse_df.to_csv(csv_loc + '/' + 'no_pulse.csv', index=False, sep= ",")
    
    
    