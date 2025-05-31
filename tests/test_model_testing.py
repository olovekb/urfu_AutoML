import pandas as pd
import pickle
import pytest
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

MODEL_PATH = "models/model.pkl"
TEST_SCALED_PATH = "data/test/test_data_scaled.csv"

@pytest.fixture(scope="module")
def load_model():
    """
    Загружает модель из модели.pkl, распаковывает кортеж
    (model, scaler_temp, scaler_humidity) и возвращает сам model.
    """
    with open(MODEL_PATH, "rb") as f:
        loaded = pickle.load(f)
    # Ожидаем, что в pickle лежит кортеж (model, scaler_temp, scaler_humidity)
    model = loaded[0]
    return model

@pytest.fixture(scope="module")
def load_test_data():
    return pd.read_csv(TEST_SCALED_PATH)

def test_model_prediction_shape(load_model, load_test_data):
    """
    Проверяет, что модель выдает такое же количество предсказаний,
    как и строк в тестовом наборе.
    """
    model = load_model
    df_test = load_test_data

    X_test = pd.DataFrame({
        "sin_day": np.sin(2 * np.pi * df_test['day'] / 30),
        "cos_day": np.cos(2 * np.pi * df_test['day'] / 30),
        "humidity": df_test['humidity']  # уже масштабированная влажность
    })
    y_test = df_test['temp']  # масштабированная температура

    y_pred = model.predict(X_test)
    assert len(y_pred) == len(y_test), "Размер предсказаний не совпадает с размером теста"

def test_model_metrics_range(load_model, load_test_data):
    """
    Проверяет, что метрики качества (MSE и R2) в адекватном диапазоне.
    """
    model = load_model
    df_test = load_test_data

    X_test = pd.DataFrame({
        "sin_day": np.sin(2 * np.pi * df_test['day'] / 30),
        "cos_day": np.cos(2 * np.pi * df_test['day'] / 30),
        "humidity": df_test['humidity']
    })
    y_test = df_test['temp']

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    assert mse >= 0, "MSE отрицательное"
    assert -1 <= r2 <= 1, "R2 вне диапазона [-1, 1]"
