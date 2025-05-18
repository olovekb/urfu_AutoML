#!/usr/bin/env python3
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

# Создаем директории для сохранения, если нет
os.makedirs("./data/train", exist_ok=True)
os.makedirs("./data/test", exist_ok=True)

# Загружаем данные
train_data = pd.read_csv('./data/train/train_data.csv')
test_data = pd.read_csv('./data/test/test_data.csv')

scaler_temp = StandardScaler()
scaler_humidity = StandardScaler()

# Нормализация train_data
train_data[['temp']] = scaler_temp.fit_transform(train_data[['temp']])
train_data[['humidity']] = scaler_humidity.fit_transform(train_data[['humidity']])

# Нормализация test_data
test_data[['temp']] = scaler_temp.transform(test_data[['temp']])
test_data[['humidity']] = scaler_humidity.transform(test_data[['humidity']])

# Сохраняем предобработанные данные
train_data.to_csv('./data/train/train_data_scaled.csv', index=False)
test_data.to_csv('./data/test/test_data_scaled.csv', index=False)

print("Data preprocessing completed.")
