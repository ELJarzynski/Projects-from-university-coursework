from sklearn.datasets import fetch_openml
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Pobranie zbioru danych Fashion-MNIST
X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='pandas')

# Podział zbioru danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Zdefiniowanie potoków przetwarzania wstępnego dla każdego modelu
rf_pipeline = Pipeline([
    ('preprocessing', Normalizer(norm='l2')),
    ('classification', RandomForestClassifier(random_state=42))
])

# Zdefiniowanie siatek hiperparametrów dla lasu losowego
rf_param_grid = {
    'classification__n_estimators': [16, 32, 64],
    'classification__max_features': range(4, 14, 5)
}

# Utworzenie obiektu RandomizedSearchCV dla lasu losowego
rf_random_search = RandomizedSearchCV(rf_pipeline, rf_param_grid, cv=5, scoring='accuracy', n_iter=10, random_state=42, n_jobs=-1)

# Trenowanie modelu i przeszukiwanie siatki
rf_random_search.fit(X_train, y_train)

# Wybór najlepszego modelu
best_rf_model = rf_random_search.best_estimator_

# Ocena modelu na zbiorze testowym
rf_accuracy = accuracy_score(y_test, best_rf_model.predict(X_test))
rf_precision = precision_score(y_test, best_rf_model.predict(X_test), average='macro')
rf_recall = recall_score(y_test, best_rf_model.predict(X_test), average='macro')

# Wyświetlenie wyników
print("Random Forest Accuracy:", rf_accuracy)
print("Random Forest Precision:", rf_precision)
print("Random Forest Recall:", rf_recall)
