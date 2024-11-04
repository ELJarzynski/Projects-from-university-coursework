import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
from sklearn.pipeline import make_pipeline
"""File lanching"""
file_directory: str = r"C:\Users\kamil\Desktop\Studia\Semestr VI\MachinLearning\Auta.csv"
cars = pd.read_csv(file_directory)
cars.replace('?', None, inplace=True)
"""Display of terminal setup"""
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


num_values_pipeline = make_pipeline(
    SimpleImputer(strategy='mean'),
    MinMaxScaler(),
)



from sklearn.preprocessing import OrdinalEncoder

cat_values_pipeline = make_pipeline(  # przekształcenie zmiennych kategorycznych na liczby całkowite za pomocą OrdinalEncoder
    OrdinalEncoder(handle_unknown='error'),
)


from sklearn.compose import make_column_selector, make_column_transformer

preprocessing_pipeline = make_column_transformer(
    (num_values_pipeline, make_column_selector(dtype_include='number')),
    (cat_values_pipeline, ('fuel-type', 'make', 'aspiration', ' body-style', 'drive-wheels', 'engine-location',
                           'engine-type', 'num-of-cylinders', 'fuel-system')),
)

data_preprocessed = pd.DataFrame(
    preprocessing_pipeline.fit_transform(cars),
    columns=preprocessing_pipeline.get_feature_names_out(),
    index=cars.index,
)
print(cars.info())
print(cars.head())
print(data_preprocessed.info())
print(data_preprocessed.head())
