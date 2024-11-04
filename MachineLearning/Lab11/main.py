from sklearn.datasets import fetch_openml
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import Normalizer

# GridSearchCV is the process that will try all combinations of hyperparameters defined in the grid in this grid to find
# the best combination that maximize the model's performance as evaluated by the specified scoring metric (in this case accuracy)
# on the cross-validated data.

X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='pandas')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

preprocessing_pipeline = make_pipeline(
    Normalizer(),
)

full_pipeline = Pipeline([
    ('preprocessing', preprocessing_pipeline),
    ('classification', RandomForestClassifier(random_state=42)),
])

hiperparam_grid = [
                {
                    'preprocessing__normalizer__norm': ['l1', 'l2', 'max'],
                    'classification__n_estimators': [16, 32, 64],
                    'classification__max_features': range(4, 14, 5),
                },
                {
                    'preprocessing__normalizer__norm': ['l1', 'l2', 'max'],
                    'classification__n_estimators': [64, 128, 256],
                    'classification__max_features': ['sqrt', 'log2'],
                }
            ]


grid_search = GridSearchCV(full_pipeline, hiperparam_grid, n_jobs=-1, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)
print(grid_search.score(X_test, y_test))
