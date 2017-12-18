import numpy as np 
import pandas as pd 
import os
from scipy.stats import multivariate_normal

data_folder = 'data/'

user_data = {}

for file in os.listdir(data_folder):

    df = pd.read_csv(data_folder + file)
    df = df._get_numeric_data()

    for x in df.groupby('Id'):
        if x[0] not in user_data:
            user_data[x[0]] = []

        user_data[x[0]].extend(x[1].as_matrix()[:3].flatten())

data_matrix = []

for id, data in user_data.items():
    data_matrix.append(data)

data_matrix = np.array(data_matrix, dtype=np.float64)

mean = data_matrix.mean(axis=0)
covariance = np.cov(data_matrix.T)

new_point = data_matrix[15] # SET TO NEW INPUT POINT

new_prob = multivariate_normal.pdf(new_point, mean=mean, cov=covariance);

print('probability of new point under existing data:', new_prob)