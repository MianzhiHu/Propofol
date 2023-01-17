import pickle
import numpy as np
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

    # fig = ax.get_figure()
    # fig.savefig(f"graphs/{name}_out.svg", bbox_inches='tight')


def draw_whole(results_df, name:str):
    print(results_df := results_df.mean(axis=1))
    ax = sns.lineplot(data=results_df, linestyle='-', dashes=False)
    ax.set_title(name)
    plt.figure(figsize=(50, 50))
    ax.set_ylim(-0.08, 0.08)

    ax.set(xlabel='Window No.', ylabel='Hurst (Mean of Means)')

    plt.show()

    # fig = ax.get_figure()
    # fig.savefig(f"graphs/{name}_out_whole.svg", bbox_inches='tight')


def plotting_all(pickle_name: str):
    if __name__ == '__main__':
        with open(pickle_name, 'rb') as f:
            results_duo = pickle.load(f)
        results_df_complete = pd.DataFrame.from_dict(results_duo[0], orient='index')
        results_df_complete = pd.DataFrame(results_df_complete.values-np.nanmean(results_df_complete.values, 0))
        results_df_complete.columns = results_duo[1]

        results_df_movie = results_df_complete.filter(axis=1, regex='.*movie.*')
        results_df_rest = results_df_complete.filter(axis=1, regex='.*rest.*')
        results_df_movie_90 = results_df_movie.head(90)
        results_df_rest_90 = results_df_rest.head(90)
        # results_df_rest_100.T.to_csv('rest_100.csv')
        # results_df_movie_100.T.to_csv('movie_100.csv')
        #
        # draw(results_df_complete, 'recovery')
        # draw_whole(results_df_complete, 'recovery average')
        # draw(results_df_movie, f'movie {pickle_name}')
        # draw(results_df_rest, f'rest {pickle_name}')
        # draw_whole(results_df_movie, f'movie average {pickle_name}')
        # draw_whole(results_df_rest, f'rest average {pickle_name}')
        # draw(results_df_movie_90, f'movie_90 {pickle_name}')
        # draw_whole(results_df_movie_90, f'movie_100 average {pickle_name}')
        # draw(results_df_rest_90, f'rest_90 {pickle_name}')
        # draw_whole(results_df_rest_90, f'rest_100 average {pickle_name}')

        rest_90_tests = np.vstack([ttest_ind
                                    (results_df_rest_90.values[i, :][(~np.isnan(results_df_rest_90.values[0, :])) & (~np.isnan(results_df_rest_90.values[i, :]))],
                                     results_df_rest_90.values[0, :]
                                     [(~np.isnan(results_df_rest_90.values[0, :])) &
                                      (~np.isnan(results_df_rest_90.values[i, :]))]
                                     )
                                    for i in range(results_df_rest_90.shape[0]-1)])

        plt.clf()
        plt.plot(rest_90_tests[:, 1], label='p-value', color='red')
        plt.ylabel('p-value')
        plt.axhline(0.05, color='black')
        ax = plt.twinx()
        ax.plot(rest_90_tests[:, 0], label='t-value', color='blue')
        ax.set_ylabel('t-value')
        plt.legend()
        plt.tight_layout()
        plt.title(f'Rest 90 test {pickle_name}')
        plt.show()

        movie_90_tests = np.vstack([ttest_ind
                                    (results_df_movie_90.values[i, :][(~np.isnan(results_df_movie_90.values[0, :])) & (~np.isnan(results_df_movie_90.values[i, :]))],
                                     results_df_movie_90.values[0, :]
                                     [(~np.isnan(results_df_movie_90.values[0, :])) &
                                      (~np.isnan(results_df_movie_90.values[i, :]))]
                                     )
                                    for i in range(results_df_movie_90.shape[0]-1)])

        plt.plot(movie_90_tests[:, 1], label='p-value', color='red')
        plt.ylabel('p-value')
        plt.axhline(0.05, color='black')
        ax = plt.twinx()
        ax.plot(movie_90_tests[:, 0], label='t-value', color='blue')
        ax.set_ylabel('t-value')
        plt.legend()
        plt.tight_layout()
        plt.title(f'Movie 90 test {pickle_name}')
        plt.show()
        # print(results_df_complete)
        # print(results_df_movie)
        # print(results_df_rest)



plotting_all('awake.pickle')
plotting_all('mild.pickle')
plotting_all('deep.pickle')
plotting_all('recovery.pickle')
