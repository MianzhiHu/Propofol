import scipy.io as sio
import numpy as np
import pandas as pd
from partial_least_squares import nodes_with_missing_values

# read lv_vals file
lv_vals = sio.loadmat('PLS_outputTaskPLShurst_propofol_movie_lv_vals.mat')
# print(lv_vals)
lv_vals_movie_03 = sio.loadmat('PLS_outputTaskPLSmovie_03_lv_vals.mat')
# print(lv_vals_movie_03)
lv_vals_movie_02 = sio.loadmat('PLS_outputTaskPLSmovie_02_lv_vals.mat')

# read bootstrap ratio file
boot_ratio = sio.loadmat('PLS_outputTaskPLShurst_propofol_movie.mat')
boot_ratio_movie_03 = sio.loadmat('PLS_outputTaskPLSmovie_03.mat')
boot_ratio_movie_02 = sio.loadmat('PLS_outputTaskPLSmovie_02.mat')
# print(boot_ratio)

def plot_preparation(lv_vals, boot_ratio, nodes_with_missing_values):
    # get the data with only the first column
    u1 = lv_vals['u1'][:, 0]
    # print(u1)

    # get the data
    boot_ratio = boot_ratio['bsrs1']
    # print(boot_ratio)

    # combine the data with their respective columns
    data = np.column_stack((u1, boot_ratio))
    # print(data)

    # name the columns
    df = pd.DataFrame(data, columns=['u1', 'boot_ratio'])
    # print(df)

    # keep only the rows with an absolute boot_ratio value greater than 3 and set the rest to NAN
    df.loc[abs(df['boot_ratio']) < 3, 'u1'] = np.nan
    # print(df)

    # Create a new dataframe with NaN values for all rows
    new_df = pd.DataFrame(data=np.nan, index=range(len(df)+len(nodes_with_missing_values)), columns=df.columns)

    # Use loc method to insert the deleted rows at their original position
    for i, row in enumerate(nodes_with_missing_values):
        new_df.loc[row] = np.nan

    # Update the values of the remaining rows in the new dataframe
    j = 0
    for i in range(len(new_df)):
        if i not in nodes_with_missing_values:
            new_df.iloc[i, :] = df.iloc[j, :]
            j += 1

    print(new_df)
    return new_df


# new_df = plot_preparation(lv_vals, boot_ratio, nodes_with_missing_values)
# new_df_movie_03 = plot_preparation(lv_vals_movie_03, boot_ratio_movie_03, nodes_with_missing_values)
new_df_movie_02 = plot_preparation(lv_vals_movie_02, boot_ratio_movie_02, nodes_with_missing_values)






