import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt


"""File lanching"""
file_directory: str = r"C:\Users\kamil\Desktop\Studia\Semestr VI\MachinLearning\Auta.csv"
cars = pd.read_csv(file_directory)
cars.replace('?', None, inplace=True)
"""Display of terminal setup"""
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Zad 2
cars.drop(["normalized-losses", "num-of-doors", "bore", "stroke", "horsepower", "peak-rpm", "price"],
          axis=1, inplace=True)

# Zad 3
"""Using Ordinal"""
encoder = OrdinalEncoder()
cars['make-encoder'] = encoder.fit_transform(cars[['make']])
cars['body-style-encoder'] = encoder.fit_transform(cars[[' body-style']])
cars['engine-type-encoder'] = encoder.fit_transform(cars[['engine-type']])
cars['num-of-cylinders-encoder'] = encoder.fit_transform(cars[['num-of-cylinders']])
cars['fuel-system-encoder'] = encoder.fit_transform(cars[['fuel-system']])

"""Using Hot Slut"""
hot_encoder = OneHotEncoder()
encoded_features = hot_encoder.fit_transform(cars[['fuel-type', 'aspiration', 'drive-wheels', 'engine-location']])
onehotdf = pd.DataFrame(
    encoded_features.toarray(),
    columns=hot_encoder.get_feature_names_out(['fuel-type', 'aspiration', 'drive-wheels', 'engine-location']),
    index=cars.index
)

cars.drop(['fuel-type', 'make', 'aspiration', ' body-style', 'drive-wheels', 'engine-location',
           'engine-type', 'num-of-cylinders', 'fuel-system'], axis=1, inplace=True)
cars = cars.join(onehotdf)

print(cars.head())
