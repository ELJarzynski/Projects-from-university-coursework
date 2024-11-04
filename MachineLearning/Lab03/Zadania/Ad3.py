from Lab03.Zadania.Ad2 import *
df_median = cars_pandas_copy.copy()
df_mean = cars_pandas_copy.copy()

"""Dominant"""
dominant_numbers_of_doors = df_median['num-of-doors'].mode().iloc[0]
df_median['num-of-doors'].fillna(dominant_numbers_of_doors, inplace=True)
df_mean['num-of-doors'].fillna(dominant_numbers_of_doors, inplace=True)


"""Median"""
median_normalized_losses = df_median['normalized-losses'].median()
median_bore = df_median['bore'].median()
median_stroke = df_median['stroke'].median()
median_horsepower = df_median['horsepower'].median()
median_peak_rpm = df_median['peak-rpm'].median()
median_price = df_median['price'].median()

# upload
df_median['normalized-losses'].fillna(median_normalized_losses, inplace=True)
df_median['bore'].fillna(median_bore, inplace=True)
df_median['stroke'].fillna(median_stroke, inplace=True)
df_median['horsepower'].fillna(median_horsepower, inplace=True)
df_median['peak-rpm'].fillna(median_peak_rpm, inplace=True)
df_median['price'].fillna(median_price, inplace=True)


"""Mean"""
# Przekształć wybrane kolumny do formatu liczbowego
selected_columns = ['normalized-losses', 'bore', 'stroke', 'horsepower', 'peak-rpm', 'price']
df_mean[selected_columns] = df_mean[selected_columns].apply(pd.to_numeric, errors='coerce')

mean_normalized_losses = df_mean['normalized-losses'].mean()
mean_bore = df_mean['bore'].mean()
mean_stroke = df_mean['stroke'].mean()
mean_horsepower = df_mean['horsepower'].mean()
mean_peak_rpm = df_mean['peak-rpm'].mean()
mean_price = df_mean['price'].mean()

# upload
df_mean['normalized-losses'].fillna(mean_normalized_losses, inplace=True)
df_mean['bore'].fillna(mean_bore, inplace=True)
df_mean['stroke'].fillna(mean_stroke, inplace=True)
df_mean['horsepower'].fillna(mean_horsepower, inplace=True)
df_mean['peak-rpm'].fillna(mean_peak_rpm, inplace=True)
df_mean['price'].fillna(mean_price, inplace=True)
print(df_mean.info())
