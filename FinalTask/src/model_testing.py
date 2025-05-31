#!/usr/bin/env python3

import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error, r2_score

# 1) Загружаем масштабированные данные для теста
df_test = pd.read_csv("./data/test/test_data_scaled.csv")

# 2) Формируем те же признаки, что использовались при обучении
X_test = pd.DataFrame({
    'sin_day':  np.sin(2 * np.pi * df_test['day'] / 30),
    'cos_day':  np.cos(2 * np.pi * df_test['day'] / 30),
    'humidity': df_test['humidity']
})
y_test = df_test['temp']

# 3) Загружаем сохранённый файл models/model.pkl,
#    в котором хранится кортеж (model, scaler_temp, scaler_humidity)
with open("./models/model.pkl", "rb") as f:
    loaded = pickle.load(f)

# Проверяем, что внутри лежит кортеж: модель и два скейлера
try:
    model, scaler_temp, scaler_humidity = loaded
except Exception:
    raise ValueError(
        "Неправильный формат models/model.pkl. "
        "Ожидается кортеж (model, scaler_temp, scaler_humidity)."
    )

# 4) Выполняем предсказание и оцениваем качество
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.3f}")
print(f"R^2 Score: {r2:.3f}")
