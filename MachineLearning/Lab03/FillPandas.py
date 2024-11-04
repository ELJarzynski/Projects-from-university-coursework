from sklearn.datasets import fetch_california_housing
from random import randint

data = fetch_california_housing(as_frame=True)['frame']
print(data.info())
data['MedInc'].isnull().any() # czy są wartości Nan w MedInc
data.isnull().any(axis=0) #  sprawdza czy są kolumny z wartosciami None i Nan axis 0 to kolumny


# przykladowy kod usuwajacy kilka wartosci metoda chybil-trafil
# minimalny i maksymalny odsetek komorek do usuniecia wartosci
min_percent, max_percent = 0.001, 0.003

# wyznacza pseudolosowo od 0.1 do 0.3% komórek z ramki danych
cells_to_remove = randint(int(data.size * min_percent), int(data.size * max_percent))

# pseudolosowy wybor indeksow wierszy i kolumn
for _ in range(cells_to_remove):
  row_idx = randint(0, data.shape[0] - 1)  # pseudolosowy indeks wiersza
  col_idx = randint(0, data.shape[1] - 1)  # pseudolosowy indeks kolumny

  # usuniecie pseudolosowo wskazanej komorki
  data.iat[row_idx, col_idx] = None

data.isnull().any(axis=0)
data['MedInc'].fillna(0)

# fill blank values, przekazanie słownika nie petla bo ona tworzy kopie ramki danych
data.fillna({
    'Longitude': 0,
    'Latitude': 100,
})

print(data['MedHouseVal'].mean())
data['MedHouseVal'].median()

print(data.isnull().any(axis=0))
