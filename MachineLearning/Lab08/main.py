import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score


# data = {
#     'Outlook': ['Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Sunny', 'Rainy', 'Overcast'],
#     'Temp': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild'],
#     'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High'],
#     'Windy': ['False', 'True', 'False', 'False', 'False', 'True', 'True', 'False', 'False', 'False', 'True', 'True'],
#     'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes']
# }
data = {
    'Outlook': ['Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Sunny'],
    'Temp': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal'],
    'Windy': ['False', 'True', 'False', 'False', 'False', 'True', 'True', 'False', 'False', 'False'],
    'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes']
}

df = pd.DataFrame(data)

# Konwertowanie danych kategorycznych na wartości liczbowe
df['Outlook'] = df['Outlook'].astype('category').cat.codes
df['Temp'] = df['Temp'].astype('category').cat.codes
df['Humidity'] = df['Humidity'].astype('category').cat.codes
df['Windy'] = df['Windy'].astype('category').cat.codes
df['Play'] = df['Play'].astype('category').cat.codes

# Podział danych na cechy (X) i etykiety (y)
X = df.drop('Play', axis=1)
y = df['Play']

model = DecisionTreeClassifier()
model.fit(X, y)
y_pred = model.predict(X)

"""Model test"""
testdf = pd.DataFrame({'Outlook': [1, 0], 'Temp': [2, 2], 'Humidity': [0, 1], 'Windy': [1, 1]})
predicted = model.predict(testdf)
# print(predicted)

# TP, TN, FP, FN
TP = sum((y == 1) & (y_pred == 1))
TN = sum((y == 0) & (y_pred == 0))
FP = sum((y == 0) & (y_pred == 1))
FN = sum((y == 1) & (y_pred == 0))
precision_score = precision_score(y, y_pred)
recall_score = recall_score(y, y_pred)
# print("Precision: ", precision_score)
# print("Recall: ", recall_score)
# true_value = df['Play']
# df_summary = pd.DataFrame({'predictions': y_pred, 'Actual values': true_value})
# print(df_summary)
