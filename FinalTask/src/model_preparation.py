import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle

# Убедимся, что директория для модели существует
os.makedirs("./models", exist_ok=True)

# 1) Читаем масштабированные данные и обучаем модель
df_train_scaled = pd.read_csv("./data/train/train_data_scaled.csv")
X_train = pd.DataFrame({
    'sin_day':  np.sin(2 * np.pi * df_train_scaled['day'] / 30),
    'cos_day':  np.cos(2 * np.pi * df_train_scaled['day'] / 30),
    'humidity': df_train_scaled['humidity']
})
y_train = df_train_scaled['temp']

model = LinearRegression()
model.fit(X_train, y_train)

# 2) Читаем «сырые» данные, чтобы восстановить скейлеры
df_train_raw = pd.read_csv("./data/train/train_data.csv")
scaler_temp     = StandardScaler().fit(df_train_raw[['temp']].astype(float))
scaler_humidity = StandardScaler().fit(df_train_raw[['humidity']].astype(float))

# 3) Сохраняем кортеж (model, scaler_temp, scaler_humidity)
with open("./models/model.pkl", "wb") as f:
    pickle.dump((model, scaler_temp, scaler_humidity), f)

print("Обучение модели и сохранение (model, scaler_temp, scaler_humidity) завершено.")
