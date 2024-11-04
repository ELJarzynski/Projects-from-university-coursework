import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

"""Display of terminal setup"""
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

"""Data Preparing"""
file_directory = r"C:\Users\kamil\Desktop\Studia\Semestr VI\MachinLearning\housing.csv"
housing = pd.read_csv(file_directory)

"""Data Preprocessing"""
housing = housing.dropna(subset=["total_bedrooms"])
hot_encoder = OneHotEncoder()
encoded_feature = hot_encoder.fit_transform(housing[['ocean_proximity']])
onehot_df = pd.DataFrame(
    encoded_feature.toarray(),
    columns=hot_encoder.get_feature_names_out(['ocean_proximity']),
    index=housing.index
)
housing.drop(['ocean_proximity'], axis=1, inplace=True)
housing = housing.join(onehot_df)

"""Data split"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt

X_train, y_train = housing[list(set(housing) - set('median_house_value'))], housing['median_house_value']
X_test, y_test = housing[list(set(housing) - set('median_house_value'))], housing['median_house_value']

"""Standaryzacja"""
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""Linear Regression"""
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f'Linear Regression means errors\n MSE: {mse}, RMSE: {sqrt(mse)}, MAE: {mae}')

"""BayesianRidge"""
from sklearn.linear_model import BayesianRidge
bayas_Model = BayesianRidge()
bayas_Model.fit(X_train, y_train)
y_bayas_pred = bayas_Model.predict(X_test)
mse = mean_squared_error(y_test,y_bayas_pred)
mae = mean_absolute_error(y_test, y_bayas_pred)

print(f'Bayesian Ridge means errors\n MSE: {mse}, RMSE: {sqrt(mse)}, MAE: {mae}')

"""Support Vector Regression"""
from sklearn.svm import SVR
svr_model = SVR()
svr_model.fit(X_train, y_train)
y_svr_pred = svr_model.predict(X_test)
mse = mean_squared_error(y_test, y_svr_pred)
mae = mean_absolute_error(y_test, y_svr_pred)

print(f'SVR means errors\n MSE: {mse}, RMSE: {sqrt(mse)}, MAE: {mae}')
