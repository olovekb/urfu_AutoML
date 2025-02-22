#!/usr/bin/env python3
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Загружаем масштабированные данные для обучения
df_train = pd.read_csv("train/train_data_scaled.csv")

X_train = df_train[['temp', 'humidity']]
y_train = df_train['day']

# Обучаем модель логистической регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Сохраняем обученную модель в файл
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model training completed.")
