import pickle
import numpy as np
import pandas as pd


# with open('outcome_268.pickle', 'rb') as f:
#     results_dict = pickle.load(f)
#     counter = 0
#     rest_recovery = {}
#     for key, value in results_dict.items():
#         if 'rest' in key and key.endswith('04_LPI_000.npy'):
#             rest_recovery[key] = value
#             counter += 1
#
# with open('rest_recovery.pickle', 'wb') as outfile:
#     pickle.dump(rest_recovery, outfile)
#     print('files saved to pickle')


def pls_csv(pickle_name: str):
    with open(pickle_name, 'rb') as f:
        results_dict = pickle.load(f)
        counter = 0
        # To convert a dictionary to a list of tuples, use the following:
        list_of_tuples = [(key, value) for key, value in results_dict.items()]
        # discard all the subjects with mean r_squared < 0.9
        list_of_tuples = [item for item in list_of_tuples if item[1]['r_squared'].mean() > 0.9]
        # keep only the hurst values for the subjects with mean r_squared > 0.9
        list_of_tuples = [item[1]['hurst'] for item in list_of_tuples]
        # convert the list of hurst values to a numpy array
        hurst_array = np.array(list_of_tuples)
        # transpose the array so that each row is a subject
        hurst_array = hurst_array.T
        # convert the array to a dataframe
        hurst_df = pd.DataFrame(hurst_array.T)
        print(hurst_df)
        print(hurst_df.shape)
        # convert the dataframe to a csv file
        hurst_df.to_csv(f'pls_{pickle_name}.csv', index=False, header=False)
        print(f'pls_{pickle_name} saved to disk')

# pls_csv('rest_recovery.pickle')

# # load the csv file
# awake = pd.read_csv('pls_movie_awake.csv', header=None)
# mild = pd.read_csv('pls_movie_mild.csv', header=None)
# deep = pd.read_csv('pls_movie_deep.csv', header=None)
# recovery = pd.read_csv('pls_movie_recovery.csv', header=None)
#
# # vertical stack the dataframes
# df = pd.concat([awake, mild, deep, recovery], axis=0)
# print(df)
# print(awake.shape, mild.shape, deep.shape, recovery.shape)
#
# # print columns with missing values
# nodes_with_missing_values = df.columns[df.isnull().any()]
# print(nodes_with_missing_values)
#
# # add 1 to the column index to get the node number
# nodes_with_missing_values = nodes_with_missing_values + 1
# print(nodes_with_missing_values)
#
# # remove the columns with missing values
# df = df.dropna(axis=1)
# print(df)
#
# # separate the dataframes into awake, mild, deep and recovery
# awake_clean = df.iloc[:12, :]
# mild_clean = df.iloc[12:24, :]
# deep_clean = df.iloc[24:32, :]
# recovery_clean = df.iloc[32:, :]
# print(awake_clean.shape, mild_clean.shape, deep_clean.shape, recovery_clean.shape)
#
# # save the dataframes to csv files
# awake_clean.to_csv('pls_movie_awake_clean.csv', index=False, header=False)
# mild_clean.to_csv('pls_movie_mild_clean.csv', index=False, header=False)
# deep_clean.to_csv('pls_movie_deep_clean.csv', index=False, header=False)
# recovery_clean.to_csv('pls_movie_recovery_clean.csv', index=False, header=False)

# do the same for the rest files
rest_awake = pd.read_csv('pls_rest_awake.csv', header=None)
rest_mild = pd.read_csv('pls_rest_mild.csv', header=None)
rest_deep = pd.read_csv('pls_rest_deep.csv', header=None)
rest_recovery = pd.read_csv('pls_rest_recovery.csv', header=None)

# vertical stack the dataframes
df = pd.concat([rest_awake, rest_mild, rest_deep, rest_recovery], axis=0)
print(df)
print(rest_awake.shape, rest_mild.shape, rest_deep.shape, rest_recovery.shape)

# print columns with missing values
nodes_with_missing_values = df.columns[df.isnull().any()]
print(nodes_with_missing_values)

# add 1 to the column index to get the node number
nodes_with_missing_values = nodes_with_missing_values + 1
print(nodes_with_missing_values)

# remove the columns with missing values
df = df.dropna(axis=1)
print(df)

# separate the dataframes into awake, mild, deep and recovery
rest_awake_clean = df.iloc[:16, :]
rest_mild_clean = df.iloc[16:31, :]
rest_deep_clean = df.iloc[31:42, :]
rest_recovery_clean = df.iloc[42:, :]

print(rest_awake_clean.shape, rest_mild_clean.shape, rest_deep_clean.shape, rest_recovery_clean.shape)

# save the dataframes to csv files
rest_awake_clean.to_csv('pls_rest_awake_clean.csv', index=False, header=False)
rest_mild_clean.to_csv('pls_rest_mild_clean.csv', index=False, header=False)
rest_deep_clean.to_csv('pls_rest_deep_clean.csv', index=False, header=False)
rest_recovery_clean.to_csv('pls_rest_recovery_clean.csv', index=False, header=False)












