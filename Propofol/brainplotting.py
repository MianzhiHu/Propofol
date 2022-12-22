import os
import pickle
from statistics import mean
import numpy as np
import pandas as pd
import scipy.stats as stats
from nilearn import plotting, input_data, datasets, image
from nilearn.image import index_img
import nibabel as nib
import matplotlib.pyplot as plt

# shen268_coords = pd.read_csv("shen268_coords.csv", index_col="NodeNo")
# print(shen268_coords.shape)
# print(shen268_coords.head())

rows: list = []
movie_awake_average: list = []

with open('outcome.pickle', 'rb') as f:
    results_dict = pickle.load(f)
    counter = 0
    for key, value in results_dict.items():
        # print(f'{key} row number is {value.shape[0]}')
        # rows.append(value.shape[0])
        if '16RA_01_movie_01_LPI_000.netts' in key:
            var = value
            # print(var.iloc[:, 0])
    # plt.hist(rows, bins=20)
    # plt.show()


s = var.iloc[:, 0]
# print(s)
s_array = np.array(s, dtype=np.float32)
print(s_array)


