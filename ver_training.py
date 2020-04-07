# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:48:24 2020

1. merge training set

@author: Noori Choi
"""

import os, glob
import pandas as pd
import numpy as np
from pathlib import Path

# Working directory
path = "D:/Lab/PhD thesis/Python/4_peakfind"
# csv location
csv_loc = "D:/Lab/PhD thesis/Python/test"

csv_list = glob.glob(os.path.join(path, "*.csv"))

csvs = [pd.read_csv(f, index_col=[0], parse_dates=[0]) for f in csv_list]
df_merged = pd.concat(csvs)
df_merged.to_csv(csv_loc + "/" + "alltesting.csv", sep= ",")