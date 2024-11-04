from sklearn.metrics import accuracy_score
from sklearn.metrics import balanced_accuracy_score

y_pred = (1, 0, 1, 1, 1, 1, 0, 0, 1, 1)
y_true = (1, 0, 1, 0, 1, 1, 0, 0, 1, 0)

print(accuracy_score(y_true, y_pred))

y_pred = (1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1)
y_true = (1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1)

print(balanced_accuracy_score(y_true, y_pred))

import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
)


def huber_loss(y_true, y_pred, delta=1.0):
    error = y_true - y_pred
    huber_loss = np.where(np.abs(error) < delta, 0.5 * error ** 2, delta * (np.abs(error) - 0.5 * delta))

    return np.mean(huber_loss)


y_true = np.random.rand(20)
y_pred = y_true + np.random.randn(20)

mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)
huber_val = huber_loss(y_true, y_pred)

print(f'MSE: {mse}, RMSE: {rmse}, MAE: {mae}, Huber: {huber_val}')

from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

print(f'{X}\n"Y:"\n{y}')

clf = DecisionTreeClassifier()
scores = cross_val_score(clf, X, y, cv=15)
print(f'Scores: \n{scores}')

mean = scores.mean()
std = scores.std() # Odchylenie standardowe
print(f'Mean: {mean}, stdandard deviation.: {std}')

from sklearn.metrics import confusion_matrix

y_true = np.random.randint(0, 2, 20)
y_pred = np.random.randint(0, 2, 20)

confusion_matrix(y_true, y_pred)

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(tn, fp, fn, tp)

precision = tp / (tp + fp)
sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)
global_accuracy = (tp + tn) / (tn + fp + fn + tp)
print(f'Precision: {precision}, sensitivity: {sensitivity}, specificity: {specificity}, accuracy {global_accuracy}')
