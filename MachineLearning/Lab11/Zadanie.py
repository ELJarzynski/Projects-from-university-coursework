from sklearn.datasets import fetch_openml
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer
from sklearn.metrics import accuracy_score, precision_score, recall_score

X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='pandas')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

"""Pipelines"""
rf_pipeline = Pipeline([
    ('preprocessing', Normalizer()),
    ('classification', RandomForestClassifier(random_state=42))
])

lr_pipeline = Pipeline([
    ('preprocessing', Normalizer()),
    ('classification', LogisticRegression(max_iter=1000, random_state=42))
])

knn_pipeline = Pipeline([
    ('preprocessing', Normalizer()),
    ('classification', KNeighborsClassifier())
])

"""Hiperparams"""
rf_param_grid = {
    'preprocessing__norm': ['l1', 'l2', 'max'],
    'classification__n_estimators': [16, 32, 64],
    'classification__max_features': [4, 8, 12]
}

lr_param_grid = {
    'preprocessing__norm': ['l1', 'l2', 'max'],
    'classification__C': [0.1, 1.0, 10.0]
}

knn_param_grid = {
    'preprocessing__norm': ['l1', 'l2', 'max'],
    'classification__n_neighbors': [3, 5, 7]
}

rf_grid_search = GridSearchCV(rf_pipeline, rf_param_grid, cv=5, scoring='accuracy', n_jobs=-1)
lr_grid_search = GridSearchCV(lr_pipeline, lr_param_grid, cv=5, scoring='accuracy', n_jobs=-1)
knn_grid_search = GridSearchCV(knn_pipeline, knn_param_grid, cv=5, scoring='accuracy', n_jobs=-1)

rf_grid_search.fit(X_train, y_train)
lr_grid_search.fit(X_train, y_train)
knn_grid_search.fit(X_train, y_train)

best_rf_model = rf_grid_search.best_estimator_
best_lr_model = lr_grid_search.best_estimator_
best_knn_model = knn_grid_search.best_estimator_
