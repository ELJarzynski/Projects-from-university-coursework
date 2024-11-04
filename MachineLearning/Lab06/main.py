from Lab03.Zadania.Ad1 import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing, fetch_openml
from sklearn.decomposition import PCA

# Wczytanie danych
data = fetch_california_housing(as_frame=True)['data']
print(data)
# PCA z 6 komponentami
pca = PCA(n_components=6)
data_6d = pca.fit_transform(data)
print(data_6d)
print(data_6d.shape)
# Wyświetlenie wyjaśnionego współczynnika wariancji
print(f'Pc redukcja  wymiarowości ktore posiadaja mniej głównych '
      f'wartosci\n{pca.explained_variance_ratio_}')


pca = PCA(n_components=0.95)
data_reduced = pca.fit_transform(data)
print(f'\nZredukowane wymiary do jednego: \n{data_reduced} \n rozmiar: {data_reduced.shape}')

# Wizualizacja
components = np.arange(1, data.shape[1])
variance = []

for i in components:
    pca = PCA(n_components=i)
    pca.fit_transform(data)
    variance.append(np.cumsum(pca.explained_variance_ratio_)[-1])

plt.plot(components, variance)
plt.xlabel('Liczba komponentów')
plt.ylabel('Wariancja wyjaśniona')
plt.title('PCA: Wariancja wyjaśniona w zależności od liczby komponentów')
plt.show()

# Odwrócenie procesu rzutowania
mnist = fetch_openml('mnist_784', parser='auto')

pca = PCA(n_components=0.95)
mnist_reduced = pca.fit_transform(mnist['data'])
print(mnist_reduced.shape)

# Wyświetlenie przykładowego obrazu z danych MNIST

plt.imshow(mnist['data'].iloc[0].values.reshape(28, 28), cmap='gray')
plt.title("Podstawowa")
# plt.show()
mnist_inversed = pca.inverse_transform(mnist_reduced)
mnist_inversed.shape
plt.imshow(mnist_inversed[0, ].reshape(28, 28), cmap='gray')
plt.title("Odwrócona")
# plt.show()
