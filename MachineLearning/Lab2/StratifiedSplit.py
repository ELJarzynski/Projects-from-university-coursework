import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import StratifiedShuffleSplit

data = fetch_california_housing(as_frame=True)['frame']
data_size = len(data)
half_data_size = data_size // 2
data['decision'] = np.array([0] * half_data_size + [1] * half_data_size)

splitter = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
output_col = 'decision'

for train_idx, test_idx in splitter.split(data.loc[:, data.columns != output_col], data[output_col]):
    print(f'{train_idx}\n{test_idx}\n{len(train_idx)}, {len(test_idx)}\n------------------\n')


print(data.iloc[1652])
