from sklearn.datasets import fetch_california_housing
import pandas as pd
from sklearn.datasets import fetch_openml


def get_dataset(name: str) -> pd.DataFrame:
    dataset = {
        'california-housing': fetch_california_housing,
    }

    data_subset = dataset[name]
    data = data_subset(as_frame=True)['frame']
    return data


def get_dataset2(name: str) -> pd.DataFrame:
    data = fetch_openml(name=name, as_frame=True)['frame']
    return data


temp = get_dataset2('california_housing')
print(type(temp))
print(temp)

