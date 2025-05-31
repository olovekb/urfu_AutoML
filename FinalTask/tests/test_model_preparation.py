import os
import pickle
import pytest
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "models/model.pkl"

@pytest.fixture(scope="module")
def loaded_objects():
    """Загружает содержимое model.pkl один раз для всех тестов"""
    assert os.path.exists(MODEL_PATH), f"Файл модели не найден: {MODEL_PATH}"
    with open(MODEL_PATH, "rb") as f:
        loaded = pickle.load(f)
    return loaded

def test_model_file_exists():
    """Проверка, что файл модели существует"""
    assert os.path.exists(MODEL_PATH), f"Файл модели не найден: {MODEL_PATH}"

def test_model_pkl_structure(loaded_objects):
    """
    Проверка, что в model.pkl хранится кортеж из
    (LinearRegression, StandardScaler, StandardScaler)
    """
    assert isinstance(loaded_objects, tuple), "Содержимое model.pkl должно быть кортежем"
    assert len(loaded_objects) == 3, f"Ожидается кортеж длины 3, а получена длина {len(loaded_objects)}"
    
    model, scaler_temp, scaler_humidity = loaded_objects
    assert isinstance(model, LinearRegression), "Первый элемент кортежа не является LinearRegression"
    assert isinstance(scaler_temp, StandardScaler), "Второй элемент кортежа не является StandardScaler (scaler_temp)"
    assert isinstance(scaler_humidity, StandardScaler), "Третий элемент кортежа не является StandardScaler (scaler_humidity)"

@pytest.fixture(scope="module")
def model(loaded_objects):
    """Возвращает сам объект модели LinearRegression"""
    return loaded_objects[0]

def test_model_type(model):
    """Проверка, что модель нужного класса"""
    assert isinstance(model, LinearRegression), "Модель не LinearRegression"

def test_model_coefficients_valid(model):
    """Проверка, что коэффициенты не пустые и не NaN"""
    coef = model.coef_
    assert coef is not None, "Коэффициенты модели отсутствуют"
    assert not np.isnan(coef).any(), "В коэффициентах есть NaN"
