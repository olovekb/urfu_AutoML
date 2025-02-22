#!/usr/bin/env python3
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Загружаем масштабированные данные для обучения
train_file = "train/train_data_scaled.csv"
df_train = pd.read_csv(train_file)
X_train = df_train[['day', 'temp']]
y_train = df_train['label']

# Обучаем модель логистической регрессии
model = LogisticRegression()
model.fit(X_train, y_train)

# Сохраняем обученную модель в файл
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model training completed.")
