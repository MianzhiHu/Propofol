import pickle
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression

with open('outcome_268.pickle', 'rb') as f:
    results_dict = pickle.load(f)
    counter = 0
    movie_awake = {}
    for key, value in results_dict.items():
        if 'movie' in key and key.endswith('04_LPI_000.npy'):
            movie_awake[key] = value
            counter += 1

with open('movie_recovery.pickle', 'wb') as outfile:
    pickle.dump(movie_awake, outfile)
    print('files saved to pickle')


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
        hurst_df.to_csv(f'pls_{pickle_name}.csv', index=False, header=True)
        print(f'pls_{pickle_name} saved to disk')

pls_csv('movie_recovery.pickle')






