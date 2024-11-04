import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.datasets import fetch_kddcup99
from sklearn.datasets import fetch_california_housing

"""Display of terminal setup"""
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

from sklearn.pipeline import make_pipeline
num_values_pipeline = make_pipeline(  # nie podajemy alias alias jest potrzebny do optymalizacji hiperparametrów
    SimpleImputer(strategy='mean'),
    MinMaxScaler(),
)

# data = fetch_california_housing(as_frame=True)['frame']
# num_values_pipeline.fit_transform(data)
# data_preprocessed = pd.DataFrame(
#     num_values_pipeline.fit_transform(data),
#     columns=num_values_pipeline.get_feature_names_out(),
#     index=data.index,
# )

# print(data_preprocessed)

"""Keczup"""
data = fetch_kddcup99(as_frame=True)['frame']

data[['duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent']] = data[
    ['duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent']].astype(int)

data[['protocol_type', 'service', 'flag', 'labels']] = data[['protocol_type', 'service', 'flag', 'labels']].applymap(
    lambda x: x.decode('utf-8'))  # przekształcenie wartości z binarnych na utf-8


from sklearn.preprocessing import OrdinalEncoder

cat_values_pipeline = make_pipeline(  # przekształcenie zmiennych kategorycznych na liczby całkowite za pomocą OrdinalEncoder
    OrdinalEncoder(handle_unknown='error'),
)

from sklearn.compose import make_column_selector, make_column_transformer

preprocessing_pipeline = make_column_transformer(
    (num_values_pipeline, make_column_selector(dtype_include='number')),
    (cat_values_pipeline, ('protocol_type', 'service', 'flag', 'labels')),
)
data_preprocessed = pd.DataFrame(
    preprocessing_pipeline.fit_transform(data),
    columns=preprocessing_pipeline.get_feature_names_out(),
    index=data.index,
)
print(data)
print(data_preprocessed)
