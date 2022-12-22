import os
import pickle
from statistics import mean
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from Propofol.dfa import dfa

target_dir = 'data_clean'


def read_files(directory: str):
    for file in os.listdir(directory):
        if file.endswith("_04_LPI_000.netts"):
            # 读取数据到numpy 2d array
            array_2d = np.loadtxt(os.path.join(target_dir, file), delimiter='\t')
            yield array_2d, file


def preprocess():
    tr: int = 2  # 2000 ms
    max_frequency = 0.1
    min_frequency = 0.01
    mn = int(np.ceil(1 / (tr * max_frequency)))
    mx = int(np.floor(1 / (tr * min_frequency)))
    print(f'mn: {mn}, mx: {mx}')
    counter = 0
    results_dict = {}

    min = 99999999999999999999999
    name = ''
    max = 0
    jihangjielie = {}
    for array_2d, file in read_files(directory=target_dir):
        print(df := pd.DataFrame(array_2d))

        jihangjielie[file] = df.shape
        if df.shape[1] < 100:
            print(f'skipped file {file} due to insufficient columns')
            continue
        first_slice = df.loc[:, :69]
        second_slice = df.loc[:, 70:]
        # third_slice = df.loc[:, 139:]

        # print(first_slice)
        # print(first_slice.to_numpy().shape)
        # print(first_slice.to_numpy())
        # print(second_slice.to_numpy().shape)
        # print(third_slice.to_numpy().shape)
        #print(third_slice.to_numpy().shape)
        # if third_slice.to_numpy().shape[1] < min:
        #     twomin = second_slice.to_numpy().shape[1]
        #     min = third_slice.to_numpy().shape[1]
        #     name = file
        # if third_slice.to_numpy().shape[1] > max:
        #     max = third_slice.to_numpy().shape[1]
    # print(f'min is {min}, twomin is {twomin}, name is {name}, max is {max}')
    #pprint(jihangjielie)
        dfa_results_slice1 = dfa(x=first_slice.to_numpy().T, max_window_size=mx, min_window_size=mn, return_confidence_interval=True,
                           return_windows=False)

        dfa_results_slice2 = dfa(x=second_slice.to_numpy().T, max_window_size=mx, min_window_size=mn, return_confidence_interval=True,
                           return_windows=False)
        # dfa_results_slice3 = dfa(x=third_slice.to_numpy().T, max_window_size=mx, min_window_size=mn, return_confidence_interval=True,
        #                    return_windows=False)
        # quit()
        dfa_results_slices = [dfa_results_slice1, dfa_results_slice2]#, dfa_results_slice3]
        # #
        # # dfa_results = dfa(x=array_2d.T, max_window_size=mx, min_window_size=mn, return_confidence_interval=True,
        # #                   return_windows=False)
        #
        def post_process(dfa_results):
            split_h = len(dfa_results[0])
            # turn results into a 2d array, where each column is a key
            hurst = np.hsplit(np.array(np.array(dfa_results[0])), split_h)
            print(dfa_results[0])
            print(dfa_results[1])
            print(f'length of dfa_results[0]: {len(dfa_results[0])}')
            print(f'length of dfa_results[1]: {len(dfa_results[1])}')
            cis0 = np.array([item[0] for item in dfa_results[1]])
            cis1 = np.array([item[1] for item in dfa_results[1]])
            cis0 = np.hsplit(cis0, split_h)
            cis1 = np.hsplit(cis1, split_h)
            r_squared = np.hsplit(np.array(np.array(dfa_results[2])), split_h)
            array_new = np.hstack((hurst, cis0, cis1, r_squared))
            df = pd.DataFrame(array_new, columns=['hurst', 'cis0', 'cis1', 'rsquared'])
            return df
        combined_df = []
        for dfa_results_slice in dfa_results_slices:
            combined_df.append(post_process(dfa_results=dfa_results_slice))

        results_dict[file] = combined_df
        counter += 1

        print(f'processing done for {file}')

    print('finished processing all files, saving to pickle')
    with open('2022-12-08.pickle', 'wb') as outfile:
        pickle.dump(results_dict, outfile)


if __name__ == '__main__':
    #preprocess()

    print('show results from pickle')

    movie_first_hurst_values: list = []
    rest_first_hurst_values: list = []

    with open('2022-12-08.pickle', 'rb') as f:
        results_dict = pickle.load(f)
        counter = 0
        for key, value in results_dict.items():
            if '_04' in key:
                counter += 1
                print(type(value))
                print(value)
                print(key)
                movie_first_hurst_values.append(value[0]['hurst'].mean())
                print(value[0]['hurst'][0:2].mean())

        print(movie_first_hurst_values)
        print(rest_first_hurst_values)

        # print(f'reading matrix for file 30AQ_01_rest_04_LPI_000.netts')
        # print(results_dict['30AQ_01_rest_04_LPI_000.netts'])
