# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:48:56 2020

Extreme Value Machine (EVM) using Dynamic Time Warping (DTW) distance

@author: Noori Choi
"""
import pandas as pd
import os
from pathlib import Path
import numpy as np
import EVM
from tslearn import metrics

# set directories
train = "D:/Lab/PhD thesis/Python/6_MEVM_train"
test = "D:/Lab/PhD thesis/Python/5_alltesting"
csv_loc = "D:/Lab/PhD thesis/Python/6_MEVM_alltesting"

train_path = Path(train) #train_csv directory
test_path = Path(test) #test_csv directory

train_csv = os.listdir(train_path)
test_csv = os.listdir(test_path)

#Data preparation
## Training dataset
### import csv file
index_train = []
train_data = []
for csv in train_csv:
    print("Analyzing the file " + csv)
    index_train.append(csv)
    df = pd.read_csv(train_path/csv, index_col = ["File", "bout"])
    # remove bouts including 1-2 pulses
    df = df.groupby(['File', 'bout']).filter(lambda x: len(x['Time']) >= 3)

    # Standardize amp and time
    df['amp_mx'] =  df.groupby(['File', 'bout']).apply(lambda x: x['Amp'].max())
    df['time_mn'] = df.groupby(['File', 'bout']).apply(lambda x: x['Time'].min())
    df['amp_r'] = df['Amp'] / df['amp_mx']
    df['time_r'] = df['Time'] - df['time_mn']
    #sort values
    df = df.sort_values(by=['File', 'bout', 'time_r']) 

    time_amp_dict = df.groupby(['File', 'bout'])[['time_r', 'amp_r']].apply(
        #save time_r, amp_r of each bout as array
        lambda g: g.values.tolist()
        )
    print(time_amp_dict)
    csv = [time_amp_dict[i] for i in range(len(time_amp_dict))]
    train_data.append(csv)
    train_data
    index_train

train_data # [[species1],[species2],...]
index_train

#Extreme Value Machine
## Training EVM model
mevm = EVM.MultipleEVM(tailsize=10, cover_threshold = 0.5, distance_function=metrics.dtw)
mevm.train(train_data)

## Testing dataset
for csv in test_csv:
    print("Analyzing the file " + csv)
    df = pd.read_csv(test_path/csv, index_col = ["File", "bout"])
    # remove bouts including 1-2 pulses
    df = df.groupby(['File', 'bout']).filter(lambda x: len(x['Time']) >= 3)
    
    # Standardize amp and time
    df['amp_mx'] =  df.groupby(['File', 'bout']).apply(lambda x: x['Amp'].max())
    df['time_mn'] = df.groupby(['File', 'bout']).apply(lambda x: x['Time'].min())
    df['amp_r'] = df['Amp'] / df['amp_mx']
    df['time_r'] = df['Time'] - df['time_mn']
    #sort values
    df = df.sort_values(by=['File', 'bout', 'time_r']) 
    
    #feat_col, index_col

    time_amp_dict = df.groupby(['File', 'bout'])[['time_r', 'amp_r']].apply(
        #save time_r, amp_r of each bout as array
        lambda g: g.values.tolist()
        )
    
    time_amp = [time_amp_dict[i] for i in range(len(time_amp_dict))]
    probabilities, indexes = mevm.max_probabilities(time_amp)
    
    category = [x[0] for x in indexes]
    combined = np.vstack((probabilities, category)).T
    
    index_col = pd.DataFrame(time_amp_dict.reset_index()[['File','bout']])
    probs = pd.DataFrame({'prob':combined[:, 0], 'category': combined[:, 1]})
    times = pd.DataFrame({'begin':df.groupby(['File','bout'])['Time'].min().reset_index(drop=True),
                          'end': df.groupby(['File','bout'])['Time'].max().reset_index(drop=True),
                          'File':df.groupby(['File','bout'])['File'].reset_index(drop=True)})
            
    fin_df = pd.concat([index_col, times, probs], axis=1)
    fin_df['category'] = fin_df['category'].apply(lambda x: index_train[int(x)][:-4])
    fin_df.to_csv(csv_loc + '/' + csv[:-4] + '_MEVM_wouet.csv', index=False, sep = ",")
    
#probabilities, indexes = mevm.max_probabilities(class4)
#print(probabilities)
#print(indexes)