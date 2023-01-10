import pickle
import numpy as np
import pandas
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind

sns.set_theme(style="whitegrid")


def draw(results_df, name: str):
    print(results_df)
    ax = sns.lineplot(data=results_df, linestyle='-', dashes=False)
    ax.set_title(name)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1), borderaxespad=0, fontsize='xx-small')

    plt.figure(figsize=(50, 50))

    ax.set(xlabel='Window No.', ylabel='Hurst (Mean)')
    plt.show()

    fig = ax.get_figure()
    fig.savefig(f"graphs/{name}_out.svg", bbox_inches='tight')


def draw_whole(results_df, name:str):
    print(results_df := results_df.mean(axis=1))
    ax = sns.lineplot(data=results_df, linestyle='-', dashes=False)
    ax.set_title(name)
    plt.figure(figsize=(50, 50))

    ax.set(xlabel='Window No.', ylabel='Hurst (Mean of Means)')

    plt.show()

    fig = ax.get_figure()
    fig.savefig(f"graphs/{name}_out_whole.svg", bbox_inches='tight')


if __name__ == '__main__':
    with open('recovery.pickle', 'rb') as f:
        results_duo = pickle.load(f)
    results_df_complete = pd.DataFrame.from_dict(results_duo[0], orient='index')
    results_df_complete = pd.DataFrame(results_df_complete.values-np.nanmean(results_df_complete.values, 0))
    results_df_complete.columns = results_duo[1]

    results_df_movie = results_df_complete.filter(axis=1, regex='.*movie.*')
    results_df_rest = results_df_complete.filter(axis=1, regex='.*rest.*')
    results_df_movie_100 = results_df_movie.head(100)
    results_df_rest_100 = results_df_rest.head(100)
    # results_df_rest_100.T.to_csv('rest_100.csv')
    # results_df_movie_100.T.to_csv('movie_100.csv')
    #
    # draw(results_df_complete, 'recovery')
    # draw_whole(results_df_complete, 'recovery average')
    # draw(results_df_movie, 'movie')
    # draw(results_df_rest, 'rest')
    # draw_whole(results_df_movie, 'movie average')
    # draw_whole(results_df_rest, 'rest average')
    # draw(results_df_movie_100, 'movie_100')
    # draw_whole(results_df_movie_100, 'movie_100 average')
    # draw(results_df_rest_100, 'rest_100')
    # draw_whole(results_df_rest_100, 'rest_100 average')

    rest_100_tests = np.vstack([ttest_ind
                                (results_df_rest_100.values[i, :][(~np.isnan(results_df_rest_100.values[0, :])) & (~np.isnan(results_df_rest_100.values[i, :]))],
                                 results_df_rest_100.values[0, :]
                                 [(~np.isnan(results_df_rest_100.values[0, :])) &
                                  (~np.isnan(results_df_rest_100.values[i, :]))]
                                 )
                                for i in range(results_df_rest_100.shape[0]-1)])

    plt.clf()
    plt.plot(rest_100_tests[:, 1], label='p-value', color='red')
    plt.ylabel('p-value')
    plt.axhline(0.05, color='black')
    ax = plt.twinx()
    ax.plot(rest_100_tests[:, 0], label='t-value', color='blue')
    ax.set_ylabel('t-value')
    plt.legend()
    plt.tight_layout()
    plt.show()

    movie_100_tests = np.vstack([ttest_ind
                                (results_df_movie_100.values[i, :][(~np.isnan(results_df_movie_100.values[0, :])) & (~np.isnan(results_df_movie_100.values[i, :]))],
                                 results_df_movie_100.values[0, :]
                                 [(~np.isnan(results_df_movie_100.values[0, :])) &
                                  (~np.isnan(results_df_movie_100.values[i, :]))]
                                 )
                                for i in range(results_df_movie_100.shape[0]-1)])

    plt.plot(movie_100_tests[:, 1], label='p-value', color='red')
    plt.ylabel('p-value')
    plt.axhline(0.05, color='black')
    ax = plt.twinx()
    ax.plot(movie_100_tests[:, 0], label='t-value', color='blue')
    ax.set_ylabel('t-value')
    plt.legend()
    plt.tight_layout()
    plt.show()
    # print(results_df_complete)
    # print(results_df_movie)
    # print(results_df_rest)
