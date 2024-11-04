import pandas as pd
import matplotlib.pyplot as plt
from Lab04.Zadania.Ad1 import *
from sklearn.datasets import fetch_kddcup99
from sklearn.preprocessing import OneHotEncoder # czeesto stosowane w sieciach neuronowych [0 0 0]
"""Wynikiem jest obiekt zawierający macierz rzadką, czyli taka macierz w której nie ma atrybutów 0"""
from sklearn.preprocessing import OrdinalEncoder
"""OrdinalEncoder przypisuje każdej unikalnej kategorii liczbę całkowitą, zaczynając od 0. 
                                                                      'icmp' jako 0, 'tcp' jako 1, a 'udp' jako 2."""

data = fetch_kddcup99(as_frame=True)['frame']
# print(data['protocol_type'].value_counts())
encoder = OrdinalEncoder()
labels = encoder.fit_transform(data[['protocol_type']])
# print(encoder.categories_)

encoder = OneHotEncoder()
protocol_onehot = encoder.fit_transform(data[['protocol_type']])
# print(protocol_onehot)
protocol_onehot.toarray()
# print(protocol_onehot)
# print(data.head())
onehot_df = pd.DataFrame(
    protocol_onehot.toarray(),
    columns=encoder.get_feature_names_out(),
    index=data.index
    )
data = data.join(onehot_df)  # stworzenie nowych kolumn do atrybutów z OrdinalEncoder
# print(data.head())


"""Skalowanie i transformacja atrybutów liczbowych"""
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(-1, 1))
src_bytes_scaled = scaler.fit_transform(data[['src_bytes']])
print(src_bytes_scaled)
src_bytes_scaled.max(), src_bytes_scaled.min()

"""Standaryzacja to proces polegający na wyśrodkowaniu danych oraz zachowaniu wskazanych parametrów 
                                    dotyczących rozrzutu wartości jest czuła na wartości odstające"""
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
dst_bytes_scaled = scaler.fit_transform(data[['dst_bytes']])
# print(dst_bytes_scaled)


"""Symetria wartości numerycznych"""
from sklearn.datasets import fetch_california_housing

data = fetch_california_housing(as_frame=True)['frame']


""" Powyższy histogram jest prawoskośny, co oznacza że jego asymetria jest spowodowana nasileniem występowania wartości 
    występujących po lewej stronie histogramu. Analogicznie wygląda sytuacja w przypadku lewoskośności. 
    Rozwiązaniem tego problemu może być zastosowanie skali logarytmicznej lub pierwiastkowej."""

import numpy as np
data['MedInc'].hist(bins=100)
np.sqrt(data['MedInc']).hist(bins=100)
np.log(data['MedInc']).hist(bins=100)
plt.show()
