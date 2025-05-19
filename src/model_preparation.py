import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

os.makedirs("./models", exist_ok=True)

df_train = pd.read_csv("./data/train/train_data_scaled.csv")

X_train = pd.DataFrame()
X_train['sin_day'] = np.sin(2 * np.pi * df_train['day'] / 30)
X_train['cos_day'] = np.cos(2 * np.pi * df_train['day'] / 30)
X_train['humidity'] = df_train['humidity']

y_train = df_train['temp']

# Обучаем модель
model = LinearRegression()
model.fit(X_train, y_train)

# Сохраняем модель
with open("./models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Обучение модели и сохранение завершено.")
