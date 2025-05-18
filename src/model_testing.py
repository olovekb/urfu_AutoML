#!/usr/bin/env python3
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error, r2_score

# Загружаем масштабированные данные для теста
df_test = pd.read_csv("./data/test/test_data_scaled.csv")

# Формируем те же признаки
X_test = pd.DataFrame()
X_test['sin_day'] = np.sin(2 * np.pi * df_test['day'] / 30)
X_test['cos_day'] = np.cos(2 * np.pi * df_test['day'] / 30)
X_test['humidity'] = df_test['humidity']

y_test = df_test['temp']

# Загружаем сохранённую модель
with open("./models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Выполняем предсказание и оцениваем качество
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.3f}")
print(f"R^2 Score: {r2:.3f}")
