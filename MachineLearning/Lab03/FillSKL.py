from sklearn.impute import SimpleImputer
from Lab03.FillPandas import data
import pandas as pd


imputer = SimpleImputer(strategy='median')
# Przed właściwym uzupełnieniem wartości należy najpierw wybrać zestaw pasujących atrybutów, dla których zostanie
# zastosowana wybrana strategia.
num_attributes = data.select_dtypes(include=['number'])
print(num_attributes)
num_attributes.isnull().any(axis=0)
# Wywołanie metody fit na utworzonym obiekcie pozwoli na automatyczne wyznaczenie wartości do uzupełnienia w każdym z atrybutów.
imputer.fit(num_attributes)
# W atrybucie statistics_ zawarte są wyznaczone wartości do zastąpenia brakujących według obranej strategii.
print(imputer.statistics_)

# Do zastąpienia brakujących wartości przeznaczona jest metoda transform.
new_num_attributes = imputer.transform(num_attributes)

new_num_attributes = pd.DataFrame(new_num_attributes, columns=data.columns)
print(new_num_attributes)
new_num_attributes.isnull().any(axis=0)

"""Z uwagi na różnice między interfejsami bibliotek pandas i Scikit-learn warto zwrócić uwagę na typowe aspekty interfejsu 
    aktualnie używanego narzędzia. Wykorzystywane są dwie niezależne metody: fit oraz transform. Wywołanie metody fit 
    oznacza dopasowanie do aktualnie przekazanej ramki danych i wyznaczenie na jej podstawie wartości do uzupełnienia. 
    Analogicznie wygląda sytuacja dla przekazanego atrybutu. Wywołanie metody transform spowoduje 
    faktyczne uzupełnienie brakujących wartości i zwrócenie utworzonego w ten sposób nowego obiektu będącego pełną ramką danych. 
    Warto więc mieć na uwadze, że próba wywołania metody transform po wywołaniu metody fit na innym zbiorze danych 
    może kompletnie mijać się z celem."""
