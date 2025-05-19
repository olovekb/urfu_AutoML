import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from data_creation import create_dataset  # Импортируем функцию генерации данных

def train_model():
    """
    Обучает модель линейной регрессии на данных из файла /autoML/data/train/train_data.csv.
    Если данные отсутствуют, они генерируются автоматически.
    """
    train_file = "/autoML/data/train/train_data.csv"
    if not os.path.exists(train_file):
        print(f"{train_file} не найден. Генерирую данные...")
        create_dataset(train_file, num_points=100, noise=1.0, anomaly=True)

    # Загружаем исходные данные
    df_train = pd.read_csv(train_file)
    
    # Фитим скейлеры для температуры и влажности (как в data_preprocessing.py)
    scaler_temp = StandardScaler()
    scaler_humidity = StandardScaler()
    df_train[['temp']] = scaler_temp.fit_transform(df_train[['temp']])
    df_train[['humidity']] = scaler_humidity.fit_transform(df_train[['humidity']])
    
    # Формируем признаки: синус и косинус от дня + масштабированная влажность
    X_train = pd.DataFrame()
    X_train['sin_day'] = np.sin(2 * np.pi * df_train['day'] / 30)
    X_train['cos_day'] = np.cos(2 * np.pi * df_train['day'] / 30)
    X_train['humidity'] = df_train['humidity']
    y_train = df_train['temp']
    
    # Обучаем модель линейной регрессии
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, scaler_humidity, scaler_temp

def predict_temperature(model, scaler_humidity, scaler_temp, input_day, input_humidity):
    """
    Предсказывает температуру по заданным параметрам:
      - input_day: номер дня
      - input_humidity: значение влажности (%)
    """
    # Преобразуем входную влажность в DataFrame для масштабирования
    df_humidity = pd.DataFrame({'humidity': [input_humidity]})
    scaled_humidity = scaler_humidity.transform(df_humidity)[0, 0]
    
    # Вычисляем синус и косинус дня
    sin_day = np.sin(2 * np.pi * input_day / 30)
    cos_day = np.cos(2 * np.pi * input_day / 30)
    
    # Формируем DataFrame со столбцами, аналогичными обучающим данным
    X = pd.DataFrame({
        'sin_day': [sin_day],
        'cos_day': [cos_day],
        'humidity': [scaled_humidity]
    })
    
    # Выполняем предсказание (результат – масштабированное значение температуры)
    pred_scaled = model.predict(X)[0]
    
    # Обратное масштабирование предсказанного значения температуры
    df_temp = pd.DataFrame({'temp': [pred_scaled]})
    pred_original = scaler_temp.inverse_transform(df_temp)[0, 0]
    
    return pred_original
