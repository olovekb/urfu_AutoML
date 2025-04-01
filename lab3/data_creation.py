#!/usr/bin/env python3
import numpy as np
import pandas as pd
import os

def create_dataset(file_path, num_points=100, noise=1.0, anomaly=False):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    days = np.arange(num_points)
    # Синусоидальная зависимость температуры с добавлением шума
    temp = 10 + 10 * np.sin(2 * np.pi * days / 30) + np.random.normal(0, noise, size=num_points)
    if anomaly:
        # Добавляем аномалии (спайки)
        num_anomalies = max(1, num_points // 20)
        indices = np.random.choice(num_points, num_anomalies, replace=False)
        temp[indices] += np.random.normal(20, 5, size=num_anomalies)
    # Генерация случайной влажности (от 30% до 90%)
    humidity = np.random.uniform(30, 90, size=num_points)
    
    df = pd.DataFrame({"day": days, "temp": temp, "humidity": humidity})
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    # Пример генерации данных для обучения
    create_dataset("train/train_data.csv", num_points=100, noise=1.0, anomaly=True)
