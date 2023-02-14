import matplotlib
from matplotlib import pyplot as plt
from atlasTransform.atlasTransform.utils.atlas import load_shen_268
from nilearn import plotting, datasets, surface, image
import nipype
import scipy.io as sio
import numpy as np
import pandas as pd

# load the shen atlas
atlas = load_shen_268(1)

# read lv_vals file
lv_vals = sio.loadmat('PLS_outputTaskPLShurst_propofol_movie_lv_vals.mat')
print(lv_vals)

# get the data with only the first column
u1 = lv_vals['u1'][:, 0]
print(u1)

# read bootstrap ratio file
boot_ratio = sio.loadmat('PLS_outputTaskPLShurst_propofol_movie.mat')
print(boot_ratio)

# get the data
boot_ratio = boot_ratio['bsrs1']
print(boot_ratio)

# combine the data with their respective columns
data = np.column_stack((u1, boot_ratio))
print(data)

# name the columns
df = pd.DataFrame(data, columns=['u1', 'boot_ratio'])
print(df)

# keep only the rows with an absolute boot_ratio value greater than 3 and set the rest to NAN
df.loc[abs(df['boot_ratio']) < 3, 'u1'] = np.nan
print(df)







