#!/usr/bin/env python3
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score

# Загружаем масштабированные данные для теста
test_file = "test/test_data_scaled.csv"
df_test = pd.read_csv(test_file)
X_test = df_test[['day', 'temp']]
y_test = df_test['label']

# Загружаем сохраненную модель
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Выполняем предсказание и вычисляем accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model test accuracy is: {acc:.3f}")
