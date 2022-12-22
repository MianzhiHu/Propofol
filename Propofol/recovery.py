import os
import pickle
from pprint import pprint
import numpy as np
import pandas as pd
from Propofol.dfa import dfa

target_dir = 'data_clean'

def read_files(directory: str):
    for file in os.listdir(directory):
        if file.endswith("_04_LPI_000.netts"):
            # load data as numpy 2d array
            array_2d = np.loadtxt(os.path.join(target_dir, file), delimiter='\t')
            yield array_2d, file



def recovery_process(dfa_results):
    split_h = len(dfa_results[0])
    # turn results into a 2d array, where each column is a key
    hurst = np.hsplit(np.array(np.array(dfa_results[0])), split_h)
    cis0 = np.array([item[0] for item in dfa_results[1]])
    cis1 = np.array([item[1] for item in dfa_results[1]])
    cis0 = np.hsplit(cis0, split_h)
    cis1 = np.hsplit(cis1, split_h)
    r_squared = np.hsplit(np.array(np.array(dfa_results[2])), split_h)
    array_new = np.hstack((hurst, cis0, cis1, r_squared))
    df = pd.DataFrame(array_new, columns=['hurst', 'cis0', 'cis1', 'rsquared'])
    return df


def preprocess():
    tr: int = 2  # 2000 ms
    max_frequency = 0.1
    min_frequency = 0.01
    mn = int(np.ceil(1 / (tr * max_frequency)))
    mx = int(np.floor(1 / (tr * min_frequency)))
    print(f'mn: {mn}, mx: {mx}')
    results = {}
    processed_counter = 0
    files_processed = []

    for array_2d, file in read_files(directory=target_dir):
        if not file.endswith('_04_LPI_000.netts'):
            continue
        processed_counter += 1
        files_processed.append(file)
        print(df := pd.DataFrame(array_2d))


        def sliding_window_generator(dataframe: pd.DataFrame, window_size: int, step_size: int):
            """
            dataframes: 2d arrays from netts file
            window_size: number of columns to be included in each window
            step_size: number of columns to be skipped between each window
            number of sliding windows = (len(dataframe) - window_size) / step_size + 1
            """
            for i in range(0, dataframe.shape[1] - window_size + 1, step_size):
                yield dataframe.iloc[:, i:i + window_size]

        for window_number, df_slice in enumerate(sliding_window_generator(df, 60, step_size=1)):
            print(f'working on window {window_number} of file {file}')
            slice_dfa_result = dfa(x=df_slice.to_numpy().T, max_window_size=mx, min_window_size=mn,
                                     return_confidence_interval=True,
                                     return_windows=False)

            rec_result = recovery_process(dfa_results=slice_dfa_result)
            mean_hurst = rec_result['hurst'].mean()

            results.setdefault(window_number, []).append(mean_hurst)

        print(f'processing done for {file}')
        print('filling in missing values for counter = ', processed_counter)
        for k, v in results.items():
            if len(v) < processed_counter:
                results[k].append(np.nan)
        print(results)

    print('finished processing all files, saving to pickle')
    with open('recovery.pickle', 'wb') as outfile:
        pickle.dump([results, files_processed], outfile)


if __name__ == '__main__':
    # preprocess()
    with open('recovery.pickle', 'rb') as infile:
        results, files = pickle.load(infile)
        counter = 0
        # print(results)
        # print(files)
        print(len(files))
