# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 19:49:36 2020

1. merge csv for verification of data processing

@author: Noori Choi
"""

import os, glob, random
import pandas as pd
import numpy as np
from pathlib import Path

# Working directory
path = "D:/Lab/PhD thesis/Python/4_peakfind"
# csv location
csv_loc = "D:/Lab/PhD thesis/Python/analysis/5_grouping"

iteration = np.arange(100) #set the number of iteration
csv_list = glob.glob(os.path.join(path, "data_*.csv"))

for i in iteration:
    randoms = random.sample(csv_list, k=20) #randomly chose 20 csvs
    random_files = [pd.read_csv(f, index_col=[0], parse_dates=[0]) for f in randoms]
    df_merged = pd.concat(random_files, ignore_index=True)
    df_merged.to_csv(csv_loc + "/" + i + "_merged.csv")