# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 21:20:19 2020

1. K-medoids clustering with bouts which are not included in any EVM vectors
(inclusion probability < 0.1)

@author: Noori Choi
"""
import pandas as pd
import os
from pathlib import Path
import numpy as np
from tslearn import metrics
from tslearn.clustering import silhouette_score
from pyclustering.cluster.kmedoids import kmedoids
from random import sample
from pyclustering.utils.metric import distance_metric, type_metric
from kneed import KneeLocator

# set directories
wd = "D:/Lab/PhD thesis/Python/6_MEVM_alltesting"
root_path = Path(wd)
csv_list = os.listdir(wd)
# Source csvs
srd = "D:/Lab/PhD thesis/Python/5_alltesting"
src_path = Path(srd)
sr_csvs = os.listdir(srd)

csv_loc = "D:/Lab/PhD thesis/Python/8_kmedoids"

for csv in csv_list:
    print("Analyzing the file " + csv)

    # Data preparation
    df = pd.read_csv(root_path/csv)
    df = df[df['prob'] < 0.1] #subset of df including non-identified bouts
    files = df[['File', 'bout']].drop_duplicates().to_numpy()
    
    for sr_csv in sr_csvs:
        sr_df = pd.read_csv(src_path/sr_csv)
        
        no_id = []
        for file in files:
            sr_csv = sr_df[(sr_df['File'] == file[0]) &
                       (sr_df['bout'] == file[1])]    
            no_id.append(sr_csv)
        no_ids = pd.concat(no_id, ignore_index=True)
        no_ids.sort_values(by=['File', 'bout', 'Time']) 
    
    # begin and end time of each bout
    begin_end = pd.DataFrame({'begin':no_ids.groupby(['File','bout'])['Time'].min().reset_index(drop=True),
                          'end': no_ids.groupby(['File','bout'])['Time'].max().reset_index(drop=True)})
        
    # Standardize amp and time
    no_ids['amp_r'] =  no_ids.groupby(['File', 'bout']).apply(lambda x: x['Amp'] / x['Amp'].max()).reset_index(drop=True)
    no_ids['time_r'] = no_ids.groupby(['File', 'bout']).apply(lambda x: x['Time'] - x['Time'].min()).reset_index(drop=True)
    
    time_amp_dict = no_ids.groupby(['File', 'bout'])[['time_r', 'amp_r']].apply(
        #save time_r, amp_r of each bout as array
        lambda g: g.values.tolist()
        )
    index_col = pd.DataFrame(time_amp_dict.reset_index()[['File','bout']])
    time_amp = [time_amp_dict[i] for i in range(len(time_amp_dict))]
    
# k-medoid clustering
## define metric as dynamic time warping (dtw)
metric = distance_metric(type_metric.USER_DEFINED, func=metrics.dtw) 
## get the best number of initial medoids
#range_n_clusters = np.arange(2, 10, 1).tolist()

#best_k = []
#for i in range(5):
#    print(str(i+1) + 'th k-medoids clustering is going')
#    silhouette = []
#    for n_clusters in range_n_clusters:
#        initial_medoids = sample(range(len(time_amp)), k=n_clusters) # choose the best number of initial medoids
#        kmed = kmedoids(time_amp, initial_medoids, metric=metric)
#        kmed.process()
#        clusters = kmed.get_clusters()
        
        # generate list of cluster labels from kmed results
#        len_cluster = sum([len(cluster) for cluster in clusters])
#        clusters_df = pd.DataFrame(np.nan, index=range(len_cluster), columns=['cluster'])
        
#        for i in range(len(clusters)):
#            clusters_df['cluster'].iloc[clusters[i]] = i
#            cluster_list = clusters_df['cluster'].tolist()
            
#        silhouette_avg = silhouette_score(time_amp, cluster_list)
#        silhouette.append([n_clusters, silhouette_avg])
    
#    silhouette = np.array(silhouette)    
#    silhouette_df = pd.DataFrame({'n_cluster': silhouette[:, 0], 'values': silhouette[:, 1]})
#    kn = KneeLocator(silhouette_df['n_cluster'], silhouette_df['values'], 
#                     curve='convex', direction='decreasing', online=False)
    
#    best_k.append(kn.knee)

#print(best_k)
#fin_k = max(set(best_k), key=best_k.count)

# kmed with best_k
#initial_medoids = sample(range(len(time_amp)), k=int(fin_k))
initial_medoids = sample(range(len(time_amp)), k=4)        
fin_kmed = kmedoids(time_amp, initial_medoids, metric=metric)
fin_kmed.process()
clusters = fin_kmed.get_clusters()
medoids = fin_kmed.get_medoids()
# data frame with cluster label
len_cluster = sum([len(cluster) for cluster in clusters])
clusters_df = pd.DataFrame(np.nan, index=range(len_cluster), columns=['cluster', 'medoids'])

for i in range(len(clusters)):
    clusters_df['cluster'].iloc[clusters[i]] = i
    clusters_df['medoids'].iloc[medoids[i]] = i

fin_df = pd.concat([index_col, begin_end, clusters_df], axis=1)
fin_df.to_csv(csv_loc + '/' + 'unidentified_kmed.csv', index=False, sep = ",")
