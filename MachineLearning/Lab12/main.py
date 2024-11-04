import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.utils import plot_model

"""Display of terminal setup"""
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

"""File finding"""
file_directory = r"C:\Users\kamil\Desktop\Studia\Semestr VI\MachinLearning\winequalityN.csv"

# Corrected line
df = pd.read_csv(file_directory)

print(df.head(5))
df.isna().sum()

df = df.dropna()
df.isna().sum()

df['is_white_wine'] = [1 if typ == 'white' else 0 for typ in df['type']]

df.head()

df['is_good_wine'] = [1 if quality >= 6 else 0 for quality in df['quality']]
df.drop('quality', axis=1, inplace=True)
df.drop('type', axis=1, inplace=True)

print(df.head())
X = df.drop('is_good_wine', axis=1)
y = df['is_good_wine']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("No to tego ten")
print(X_train)
print(y_train)
print("i tam tego")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(X_train_scaled)

print("\n W koncu siec nuronowa")
tf.random.set_seed(42)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])

model.compile(
    loss=tf.keras.losses.binary_crossentropy,
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.03),
    metrics=[
        tf.keras.metrics.BinaryAccuracy(name='accuracy'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
    ],
)

model.build(X_train_scaled.shape)

model.summary()

plot_model(model, show_shapes=True)
history = model.fit(X_train_scaled, y_train, epochs=50)

print("Wizualizacja efektów treningu")
rcParams['figure.figsize'] = (18, 8)

plt.plot(
    np.arange(1, 51),
    history.history['loss'], label='Loss'
)
plt.plot(
    np.arange(1, 51),
    history.history['accuracy'], label='Accuracy'
)
plt.plot(
    np.arange(1, 51),
    history.history['precision'], label='Precision'
)
plt.plot(
    np.arange(1, 51),
    history.history['recall'], label='Recall'
)
plt.title('Evaluation metrics', size=20)
plt.xlabel('Epoch', size=14)
plt.legend()
plt.show()
"""Predykcje"""
predictions = model.predict(X_test_scaled)

print(predictions)
