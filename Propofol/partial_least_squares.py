import pickle
import numpy as np
from sklearn.cross_decomposition import PLSRegression

with open('outcome_268.pickle', 'rb') as f:
    results_dict = pickle.load(f)
    counter = 0
    for key, value in results_dict.items():
        # print(key)
        # print(value)
        # To stack all the hurst values as a row vector
        if counter == 0:
            y = np.array(value['hurst'])
            counter += 1
        else:
            y = np.vstack((y, value['hurst']))
    print(y)



    # Create dummy variables for the 'group' variable
    dummies = pd.get_dummies(df['group'])

    # Convert the dummy variables into a NumPy array
    contrast_matrix = np.asarray(dummies)


