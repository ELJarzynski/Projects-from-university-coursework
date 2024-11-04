from Lab04.Zadania.Ad1 import *
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


MinMaxScaler = MinMaxScaler(feature_range=(-1, 1))
StandardScaler = StandardScaler()

"""Standaryzacja Symboling"""
symboling_scaled = MinMaxScaler.fit_transform(cars[['symboling']])
symboling_scaled_df = pd.DataFrame(symboling_scaled, columns=['symboling'])
# symboling_scaled_df.hist(bins=3)

"""Normalizacja Wheel Base"""

wheel_base_scaler = StandardScaler.fit_transform(cars[['wheel-base']])
wheel_base_scaler_df = pd.DataFrame(wheel_base_scaler, columns=['wheel-base'])
# wheel_base_scaler_df.hist(bins=10)

"""Standaryzacja Length"""
length_scaled = MinMaxScaler.fit_transform(cars[['length']])
length_scaled_df = pd.DataFrame(length_scaled, columns=['length'])
# length_scaled_df.hist(bins=10)

"""Standaryzacja Width"""
width_scaled = MinMaxScaler.fit_transform(cars[['width']])
width_scaled_df = pd.DataFrame(width_scaled, columns=['width'])
# width_scaled_df.hist(bins=10)

"""Standaryzacja Height"""
height_scaled = MinMaxScaler.fit_transform(cars[['height']])
height_scaled_df = pd.DataFrame(height_scaled, columns=['height'])
# height_scaled_df.hist(bins=10)

"""Normalizacja Curb Weight"""
curb_weight_scaler = StandardScaler.fit_transform(cars[['curb-weight']])
curb_weight_scaler_df = pd.DataFrame(curb_weight_scaler, columns=['curb-weight'])
# curb_weight_scaler_df.hist(bins=10)

"""Normalizacja Engine Size"""
engine_size_scaler = StandardScaler.fit_transform(cars[['engine-size']])
engine_size_scaler_df = pd.DataFrame(engine_size_scaler, columns=['engine-size'])
# engine_size_scaler_df.hist(bins=10)

"""Normalizacja comperssion ratio"""
compression_ratio_scaler = StandardScaler.fit_transform(cars[[' compression-ratio']])
compression_ratio_scaler_df = pd.DataFrame(compression_ratio_scaler, columns=[' compression-ratio'])
# compression_ratio_scaler_df.hist(bins=10)

"""Normalizacja city mpg"""
city_mpg_scaler = StandardScaler.fit_transform(cars[['city-mpg']])
city_mpg_scaler_df = pd.DataFrame(city_mpg_scaler, columns=['city-mpg'])
# city_mpg_scaler_df.hist(bins=10)

"Standaryzacja Highway mpg"
highway_mpg_scaled = MinMaxScaler.fit_transform(cars[['highway-mpg']])
highway_mpg_scaled_df = pd.DataFrame(highway_mpg_scaled, columns=['highway-mpg'])
# highway_mpg_scaled_df.hist(bins=10)


cars['symboling'] = symboling_scaled_df['symboling']
cars['wheel-base'] = wheel_base_scaler_df['wheel-base']
cars['length'] = length_scaled_df['length']
cars['width'] = width_scaled_df['width']
cars['height'] = height_scaled_df['height']
cars['curb-weight'] = curb_weight_scaler_df['curb-weight']
cars['engine-size'] = engine_size_scaler_df['engine-size']
cars[' compression-ratio'] = compression_ratio_scaler_df[' compression-ratio']
cars['city-mpg'] = city_mpg_scaler_df['city-mpg']
cars['highway-mpg'] = highway_mpg_scaled_df['highway-mpg']
print(cars.head())
