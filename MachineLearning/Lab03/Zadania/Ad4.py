from sklearn.impute import SimpleImputer
from Lab03.Zadania.Ad2 import *

median_imputer = SimpleImputer(strategy='median')
mean_imputer = SimpleImputer(strategy='mean')

num_attributes = cars_sklearn_copy.select_dtypes(include=['number'])
num_attributes.isnull().any(axis=0)

# Dopasowanie imputerów do danych
median_imputer.fit(num_attributes)
mean_imputer.fit(num_attributes)

# Transformacja danych
median_new_num_attributes = median_imputer.transform(num_attributes)
mean_new_num_attributes = mean_imputer.transform(num_attributes)

# Tworzenie nowych ramion danych z uzupełnionymi wartościami
median_new_num_attributes = pd.DataFrame(median_new_num_attributes, columns=num_attributes.columns)
mean_new_num_attributes = pd.DataFrame(mean_new_num_attributes, columns=num_attributes.columns)

df_median = pd.DataFrame(median_new_num_attributes, columns=num_attributes.columns)
df_mean = pd.DataFrame(mean_new_num_attributes, columns=num_attributes.columns)
print(df_median.info())
print(df_mean.info())
