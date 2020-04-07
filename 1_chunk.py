# -*- coding: utf-8 -*-
"""
created on Wed Nov 20

First part of data analysis
1. make 10-min chunks

@author: Noori Choi
"""

# Library import
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import matplotlib

matplotlib.use('Agg')
# Working directory
wd = "D:/Lab/PhD thesis/Python/test_result"
# List of sound files
sounds = os.listdir(wd)
# Directory to save chunks
dr = "D:/Lab/PhD thesis/Python/test"
# set chunk length in ms
chunk_length_ms = 600000

for s in sounds:
    raw = AudioSegment.from_file(wd + '/' + s, format = "wav")
    chunks = make_chunks(raw, chunk_length_ms)

    for i, chunk in enumerate(chunks):
        chunk.export(dr + '/' + s + "chunk{0}.wav".format(i),format="wav")

