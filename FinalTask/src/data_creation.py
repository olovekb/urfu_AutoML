import numpy as np
import pandas as pd
import os

os.makedirs("./data/train", exist_ok=True)
os.makedirs("./data/test", exist_ok=True)


cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
          "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]

def create_dataset(file_path, num_points=100, noise=0.5, anomaly=False):
    days = np.arange(num_points)
    temp = 10 + 10 * np.sin(2 * np.pi * days / 30) + np.random.normal(0, noise, size=num_points)
    if anomaly:
        num_anomalies = max(1, num_points // 20)
        indices = np.random.choice(num_points, num_anomalies, replace=False)
        temp[indices] += np.random.normal(20, 5, size=num_anomalies)

    humidity = np.random.uniform(30, 90, size=num_points)
    city = np.random.choice(cities, size=num_points)

    df = pd.DataFrame({"day": days, "temp": temp, "humidity": humidity, "city": city})
    df.to_csv(file_path, index=False)

# Вызов функции с правильными путями
create_dataset("./data/train/train_data.csv", num_points=100, noise=1.0, anomaly=True)
create_dataset("./data/test/test_data.csv", num_points=100, noise=1.0, anomaly=False)

print("Создание данных прошло успешно.")
