from sklearn.datasets import fetch_california_housing, fetch_openml
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import fetch_openml


#ZAD1
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
# print(temp)
# print(type(temp))


def plot(train, test, title, decision):
    fig, axes = plt.subplots(1, 2)

    ax = axes[0]
    ax.hist(train[decision], color='red', alpha=0.7)
    ax.set_title('Training subset')
    ax.set_xlabel('Decision value')
    ax.set_ylabel('Amount')

    ax = axes[1]
    ax.hist(test[decision], color='green', alpha=0.7)
    ax.set_title('Test subset')
    ax.set_xlabel('Decision value')
    ax.set_ylabel('Amount')

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


# ZAD 2
data = fetch_california_housing(as_frame=True)["frame"]
X_train, X_val = train_test_split(temp, test_size=0.2, random_state=42)
X_train_trimmed, X_val_trimmed = train_test_split(X_train, test_size=0.2, random_state=42)

print(f"Dataset length: {len(data)} \nSplit into full training subset: {len(X_train)} and validation subset: {len(X_val)}"
      f" \nSplit into trimmed training subset: {len(X_train_trimmed)} and validation subset: {len(X_val_trimmed)}")


# ZAD 3
X_train, X_test = train_test_split(temp, test_size=0.2, random_state=21)
print(plot(X_train_trimmed, X_val_trimmed, "Stratified Split with validation Histogram", "median_house_value"))
print(plot(X_train, X_test, "Siple Split Histogram", "ocean_proximity"))
