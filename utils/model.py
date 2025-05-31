import os
import pickle

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def train_model():
    """
    1) Проверяет, что файл models/model.pkl существует.
    2) Загружает из него кортеж (model, scaler_temp, scaler_humidity).
    3) Возвращает (model, scaler_humidity, scaler_temp) — именно в таком порядке,
       чтобы совпадало с тем, как это ожидает utils/app.py.
    """
    MODEL_PATH = os.path.join("models", "model.pkl")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Файл модели не найден: {MODEL_PATH}.\n"
            "Нужно заранее запустить src/model_preparation.py, чтобы создать model.pkl."
        )

    # Открываем pickle и ожидаем, что внутри хранения — ровно кортеж из трёх объектов
    with open(MODEL_PATH, "rb") as f:
        loaded = pickle.load(f)

    if not (isinstance(loaded, tuple) and len(loaded) == 3):
        raise ValueError(
            f"Некорректное содержимое {MODEL_PATH}. "
            "Ожидается кортеж (model, scaler_temp, scaler_humidity)."
        )

    model, scaler_temp, scaler_humidity = loaded

    # В АПП мы распакуем как model, scaler_humidity, scaler_temp
    return model, scaler_humidity, scaler_temp


def predict_temperature(model, scaler_humidity, scaler_temp, input_day, input_humidity):
    """
    Делает прогноз «оригинальной» температуры:
      - model           : обученный LinearRegression (на scaled-данных).
      - scaler_humidity : StandardScaler, обученный на 'humidity' из сырых данных.
      - scaler_temp     : StandardScaler, обученный на 'temp' из сырых данных.
      - input_day       : int (номер дня, тот же диапазон, что и при обучении).
      - input_humidity  : float (влажность в процентах, НЕ scaled).

    Алгоритм:
      1) Преобразуем input_humidity через scaler_humidity.transform(...)
      2) Вычисляем sin_day и cos_day
      3) Собираем DataFrame из трёх признаков и вызываем model.predict -> получаем pred_scaled
      4) Делаем inverse_transform(pred_scaled) через scaler_temp, чтобы вернуть предсказание в «оригинальных» градусах
      5) Возвращаем float(pred_original)
    """

    # 1) Скалируем влажность
    df_hum = pd.DataFrame({'humidity': [input_humidity]})
    try:
        scaled_humidity = scaler_humidity.transform(df_hum)[0, 0]
    except Exception as e:
        # Если что-то пошло не так при transform, сразу бросаем исключение
        raise RuntimeError(f"Ошибка при масштабировании влажности: {e}")

    # 2) Вычисляем синус и косинус дня
    sin_day = np.sin(2 * np.pi * input_day / 30)
    cos_day = np.cos(2 * np.pi * input_day / 30)

    # 3) Формируем DataFrame, состоящий из sin_day, cos_day, scaled_humidity
    X = pd.DataFrame({
        'sin_day':  [sin_day],
        'cos_day':  [cos_day],
        'humidity': [scaled_humidity]
    })

    # 4) Делаем предсказание в «scaled» пространстве
    try:
        pred_scaled = model.predict(X)[0]
    except Exception as e:
        raise RuntimeError(f"Ошибка при предсказании модели: {e}")

    # 5) Обратное масштабирование, чтобы получить значение температуры в градусах
    df_temp = pd.DataFrame({'temp': [pred_scaled]})
    try:
        pred_original = scaler_temp.inverse_transform(df_temp)[0, 0]
    except Exception as e:
        raise RuntimeError(f"Ошибка при обратном масштабировании: {e}")

    # **ОЧЕНЬ ВАЖНО**: здесь **мы ОБЯЗАТЕЛЬНО** возвращаем число, а не None
    return float(pred_original)
