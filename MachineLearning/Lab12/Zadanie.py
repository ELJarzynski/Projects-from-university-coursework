from sklearn.datasets import fetch_openml
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import Normalizer
import tensorflow as tf
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='pandas')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

y_train = y_train.astype(int)
y_test = y_test.astype(int)
preprocessing_pipeline = make_pipeline(
    Normalizer(),
)

full_pipeline = Pipeline([
    ('preprocessing', preprocessing_pipeline),
    ('classification', RandomForestClassifier(random_state=42)),
])

tf.random.set_seed(42)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.03),
    metrics=['accuracy']
)

model.build(X_train.shape)

model.summary()

print(plot_model(model, show_shapes=True))
history = model.fit(X_train, y_train, epochs=50)
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
predictions = model.predict(X_test)

print(predictions)
