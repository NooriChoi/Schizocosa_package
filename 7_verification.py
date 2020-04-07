# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:48:30 2020

1. calculate FAR and FRR

@author: Noori Choi
"""
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Working directory
wd = "D:/Lab/PhD thesis/Python/6_MEVM_alltesting_wouet"
root_path = Path(wd)
csv_list = os.listdir(wd)
# csv location
csv_loc = "D:/Lab/PhD thesis/Python/7_verification"

result = pd.DataFrame([])
for csv in csv_list:
    print("Analyzing the file " + csv)
    df = pd.read_csv(root_path/csv)
    print(len(df))
    df = df[df['prob'] > 0.5]
    print(len(df))
    species = df['category'].unique().tolist()
    species = [x[:3] for x in species]
    print(species)
    
    ver = []
    for sp in species:
        all_cat = len(df[df['category'].str.contains(sp)])
        true_bout = len(df[df['File'].str.contains(sp)])
        positive = len(df[(df['File'].str.contains(sp)) & 
                          (df['category'].str.contains(sp))])
        print(all_cat)
        print(true_bout)
        print(positive)
        
        if true_bout > 0:
            FRR = ((true_bout - positive)/true_bout)*100
            FAR = ((all_cat - positive)/all_cat)*100 
            print(FRR)
            print(FAR)
        else:
            FRR = 'NA'
            FAR = 'NA'
        
        ver.append([sp, FAR, FRR])

    csv_ver = np.hstack((ver, np.array([[csv]] * len(ver))))
    
    result = result.append(pd.DataFrame(csv_ver, columns = ['species', 'FAR', 'FRR', 'set']))

    #result.to_csv(csv_loc + '/' + csv[:-4] + '_accuracy_fin.csv', index=False, sep = ",")