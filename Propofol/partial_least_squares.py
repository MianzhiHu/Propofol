import pickle
import numpy as np
from sklearn.cross_decomposition import PLSRegression

# Load the data for the brain parcellation nodes
X = np.genfromtxt('shen268_coords.csv', delimiter=',')

with open('outcome.pickle', 'rb') as f:
    results_dict = pickle.load(f)
    counter = 0
    for key, value in results_dict.items():
        if '16RA_01_movie_01_LPI_000.netts' in key:
            print(key)
            print(value)
            y = value.to_numpy()[:, 0]
            y = np.resize(y, (268, 1))  # Resize y to have 268 samples
            print(y)


# Fit the PLS model
pls = PLSRegression(n_components=10)
pls.fit(X, y)

# Use the model to predict the brain activity
y_pred = pls.predict(X)

# Compute the mean squared error between the predicted and actual values
mse = np.mean((y_pred - y) ** 2)
print('Mean squared error:', mse)
