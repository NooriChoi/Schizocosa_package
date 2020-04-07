# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:08:28 2020

1. calculate matchness of kmed clusters to MEVM data

@author: Noori Choi
"""
import pandas as pd
import os
from pathlib import Path
import numpy as np
from itertools import groupby, combinations

# set directories
MEVM = "D:/Lab/PhD thesis/Python/6_MEVM_alltesting"
kmed = "D:/Lab/PhD thesis/Python/8_kmedoids"
csv_loc = "D:/Lab/PhD thesis/Python/test_result"

MEVM_path = Path(MEVM) #MEVM_csv directory
kmed_path = Path(kmed) #kmed_csv directory

MEVM_csv = os.listdir(MEVM_path)
kmed_csv = os.listdir(kmed_path)

MEVM_key = 'MEVM'
kmed_key = 'kmed'

csvs = [*MEVM_csv, *kmed_csv]
csvs.sort()
joined_csv = [list(i) for j, i in groupby(csvs, lambda a: a.split('_')[0])] 

for csvs in joined_csv:
    # read csvs
    MEVM = [i for i in csvs if MEVM_key in i][0]
    kmed = [i for i in csvs if kmed_key in i][0]
    
    df_MEVM = pd.read_csv(MEVM_path/MEVM)
    df_kmed = pd.read_csv(kmed_path/kmed)
    
    # Join csvs
    df_MEVM = pd.DataFrame(df_MEVM[['File','bout','category', 'prob']])
    df_kmed = pd.DataFrame(df_kmed[['File','bout','cluster']])
    df_total = df_MEVM.merge(df_kmed, how='left', on=['File', 'bout'])
    
    sp_list = df_total.category.unique().tolist()
    
    # calculate proportions
    df_total = df_total[df_total['cluster'].notnull()]
    probs = df_total.groupby(['cluster','category']).agg({'prob':['mean','count','median','max','min']})
    print(probs)