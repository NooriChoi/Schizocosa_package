# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 14:42:37 2019

Fourth part of data analysis
1. Merge csv files from chunks into a date file

@author: Noori Choi
"""
# Combine csv files from same recording file
import os
from pathlib import Path
import pandas as pd
import numpy as np

wd = "D:/Lab/PhD thesis/Python/test"
root_path = Path(wd)
csv_list = os.listdir(wd)
# csv location
csv_loc = "D:/Lab/PhD thesis/Python/test_result"

df = pd.concat([pd.read_csv(root_path/csv) for csv in csv_list])

# generate columns with file_info
file_info = df['File'].str.rsplit("_")
df['date'] = file_info.str[0]
df['mic'] = file_info.str[1]
df['period'] = file_info.str[2]
df['chunk'] = file_info.str[3].map(lambda x: x.lstrip('wavchunk'))
# calculate real_rec_time
df['rec_time'] = df['Time'] + 600*df['chunk'].astype(int)
df['rec_time'] = (
    np.where(
        df['period'] == str(8), 
        df['rec_time'], 
        np.where(df['period'] == str(160), df['rec_time'] + 28800, df['rec_time'] + 28800*2)))
     
df.to_csv(csv_loc + '/' + "F_180604.csv", index=False, encoding='utf-8-sig')
