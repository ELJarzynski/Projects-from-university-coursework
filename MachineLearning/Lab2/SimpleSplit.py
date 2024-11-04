from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.datasets import fetch_california_housing
data = fetch_california_housing(as_frame=True)['frame']

X = np.arange(80).reshape((20, 4))  # tablica zawierajace atrybuty warunkowe
# y = range(5)  # tablica zawierajaca jeden atrybut decyzyjny
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

len(X), len(X_train), len(X_test)
# checking if is OK
assert len(X) == len(X_train) + len(X_test)

# reshape is using for reshape size of array
X = np.arange(80).reshape((20, 4))  # tablica zawierajace atrybuty warunkowe
y = range(20)  # tablica zawierajaca jeden atrybut decyzyjny
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

len(X_train), len(y_train), len(X_test), len(y_test)

# print(X)

row_16532 = data.iloc[16532]
print(row_16532)
