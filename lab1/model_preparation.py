#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Загружаем масштабированные данные для обучения
df_train = pd.read_csv("train/train_data_scaled.csv")

# Создаем новые признаки: синус и косинус от дня
X_train = pd.DataFrame()
X_train['sin_day'] = np.sin(2 * np.pi * df_train['day'] / 30)
X_train['cos_day'] = np.cos(2 * np.pi * df_train['day'] / 30)
# Добавляем влажность (если она может влиять, хотя в данных она случайная)
X_train['humidity'] = df_train['humidity']

y_train = df_train['temp']

# Обучаем модель линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Сохраняем обученную модель
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model training completed.")
