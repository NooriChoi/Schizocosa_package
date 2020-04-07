# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:52:43 2020

1. create dendrogram based on the results of MEVM and K-medoids

@author: Noori Choi
"""
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import os
from pathlib import Path
import numpy as np
from tslearn import metrics
from scipy.spatial.distance import squareform
from itertools import groupby, combinations
from sklearn.metrics import pairwise_distances_argmin_min

# set directories
grouping = "D:/Lab/PhD thesis/Python/5_alltesting"
MEVM = "D:/Lab/PhD thesis/Python/6_MEVM_alltesting_wouet"
kmed = "D:/Lab/PhD thesis/Python/8_kmedoids_wouet"
csv_loc = "D:/Lab/PhD thesis/Python/9_dendrogram"

group_path = Path(grouping) #group_csv directory
MEVM_path = Path(MEVM) #MEVM_csv directory
kmed_path = Path(kmed) #kmed_csv directory

group_csv = os.listdir(group_path)
MEVM_csv = os.listdir(MEVM_path)
kmed_csv = os.listdir(kmed_path)

group_key = 'grouping'
MEVM_key = 'MEVM'
kmed_key = 'kmed'

csvs = [*group_csv, *MEVM_csv, *kmed_csv]
csvs.sort()
joined_csv = [list(i) for j, i in groupby(csvs, lambda a: a.split('_')[0])] 

for csvs in joined_csv:
    # read csvs
    group = [i for i in csvs if group_key in i][0]
    MEVM = [i for i in csvs if MEVM_key in i][0]
    kmed = [i for i in csvs if kmed_key in i][0]
    
    df = pd.read_csv(group_path/group, index_col = ["File", "bout"])
    df_MEVM = pd.read_csv(MEVM_path/MEVM)
    df_kmed = pd.read_csv(kmed_path/kmed)
    
    print("Analyzing the file " + group)
    
    # make a time_amp lists from bout_grouping csv
    ## remove bouts including 1-2 pulses
    df = df.groupby(['File', 'bout']).filter(lambda x: len(x['Time']) >= 3)
    
    ## Standardize amp and time
    df['amp_mx'] =  df.groupby(['File', 'bout']).apply(lambda x: x['Amp'].max())
    df['time_mn'] = df.groupby(['File', 'bout']).apply(lambda x: x['Time'].min())
    df['amp_r'] = df['Amp'] / df['amp_mx']
    df['time_r'] = df['Time'] - df['time_mn']
    ## sort values
    df = df.sort_values(by=['File', 'bout', 'time_r']) 
    
    time_amp_dict = df.groupby(['File', 'bout'])[['time_r', 'amp_r']].apply(
        #save time_r, amp_r of each bout as array
        lambda g: g.values.tolist()
        )
    time_amp = [time_amp_dict[i] for i in range(len(time_amp_dict))]
    
    # Join csvs
    df_MEVM = pd.DataFrame(df_MEVM[df_MEVM['prob'] > 0.1][['File','bout','category']])
    df_kmed = pd.DataFrame(df_kmed[['File','bout','cluster']])
    ##left join
    df_woID = time_amp_dict.reset_index()
    df_woID.columns = ['File', 'bout', 'time_amp']
    df_wID = df_woID.merge(df_MEVM, how='left', on=['File', 'bout'])
    df_wID = df_wID.merge(df_kmed, how='left', on=['File', 'bout'])
    df_wID['ID'] = df_wID['File'].str.cat(df_wID['bout'].astype(str), sep="_")
    ##concaterate MEVM, kmed results
    df_wID['sound_type'] = df_wID['category'].combine_first(df_wID['cluster']) 
    df_wID = df_wID.drop(columns=['category','cluster']) #drop MEVM, kmed class
    st_list = df_wID.sound_type.unique().tolist()
    
    XY_cdist = []
    for st in st_list:
        print("processing pairwise distance between " + str(st))
        X = df_wID[df_wID['sound_type']==st]
        X_time_amp = X['time_amp'].to_list()
        XY_dist = []
        for ost in st_list:
            print("and " + str(ost))
            Y = df_wID[df_wID['sound_type']==ost]        
            Y_time_amp = Y['time_amp'].to_list()
            
            dist = np.median(metrics.cdist_dtw(X_time_amp, Y_time_amp), axis=1)
            print(dist)
            print(np.median(dist))
        
            XY_dist.append(np.median(dist))
        
        XY_cdist.append(XY_dist)
    print(XY_cdist)
    
    # make a distance metrix
    linkage_matrix = linkage(XY_cdist, "ward")
    
    # plot a dendrogram
    plt.figure(figsize=(30, 25))
    # create a color palette 
    
    dendrogram(
        linkage_matrix,
        orientation='left',
        labels=st_list,
        leaf_font_size=20.,  # font size for the x axis labels
        color_threshold=25, 
        above_threshold_color='grey'
    )
    
    plt.savefig(csv_loc + '/' + 'dendrogram_alltesting_woUet.png')