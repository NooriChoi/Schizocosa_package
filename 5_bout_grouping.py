# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 22:23:26 2020

Fifth part of data analysis
1. Gaussian Mixture Model (GMM) for bout grouping

@author: Noori Choi
"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn import mixture

# Working directory
wd = "D:/Lab/PhD thesis/Python/test"
root_path = Path(wd)
csv_list = os.listdir(wd)
# Directory where to save the csv file, must be different with wd
csv_loc = "D:/Lab/PhD thesis/Python/5_alltesting"

for csv in csv_list:
    print("Analyzing the file " + csv)

    # Data preparation
    df = pd.read_csv(root_path/csv)
    #df = df[df['File'] != 'test']
    df = df.groupby('File').apply(lambda x: x.sort_values(by=['Time'])).reset_index(drop = True) #sort by file(=mic) and Time
    df['dT'] = df.groupby('File')['Time'].diff().fillna(0) #calculate time interval
    
    df_index = df.reset_index(drop = True)
    df_dt = df[['dT']]
    
    # Gaussian Mixture Model
    outlier = 60 # set outlier max limit
    interval = df[['dT']].loc[df['dT'] < outlier]
    bout_gen = mixture.GaussianMixture(n_components=3, covariance_type='spherical') #GMM model
    bout_gen.fit(interval) #GMM model fit
    probs = bout_gen.predict_proba(df_dt) #Soft clustering
    
    probs_df = pd.DataFrame(data=probs, columns=['1', '2', '3'])
    probs_df['group'] = probs_df.idxmax(axis=1) #assign dT into the highest probability
    fin_df = pd.concat([df_index, probs_df], axis=1)
    
    med_df = fin_df[fin_df['dT']!=0].groupby('group')['dT'].median()#.nsmallest(2)
    criteria = med_df.idxmax()
    
    # Bout grouping by the largest group of dT
    fin_df['bout'] = (fin_df['group'] == criteria).groupby(fin_df['File']).cumsum() + 1
    
    fin_df.to_csv(csv_loc + '/' + csv[:-4] + '_grouping.csv', index=False, sep = ",")