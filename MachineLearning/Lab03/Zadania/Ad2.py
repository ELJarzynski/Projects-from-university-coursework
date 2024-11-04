from Lab03.Zadania.Ad1 import *
from copy import deepcopy

"""Changing '?' values into None values"""
cars.replace('?', None, inplace=True)
cars_pandas_copy = deepcopy(cars)
cars_sklearn_copy = deepcopy(cars)



