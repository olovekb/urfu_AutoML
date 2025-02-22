#!/usr/bin/env python3
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Загрузка данных
train_data = pd.read_csv('train/train_data.csv')
test_data = pd.read_csv('test/test_data.csv')

# Создание экземпляров StandardScaler
scaler_temp = StandardScaler()
scaler_humidity = StandardScaler()

# Нормализация температуры и влажности train_data
train_data[['temp']] = scaler_temp.fit_transform(train_data[['temp']])
train_data[['humidity']] = scaler_humidity.fit_transform(train_data[['humidity']])

# Нормализация температуры и влажности test_data
test_data[['temp']] = scaler_temp.transform(test_data[['temp']])
test_data[['humidity']] = scaler_humidity.transform(test_data[['humidity']])

# Сохранение предобработанных данных
train_data.to_csv('train/train_scaled.csv', index=False)
test_data.to_csv('test/test_scaled.csv', index=False)

print("Data preprocessing completed.")
