import os
import pickle
import pytest
import numpy as np
from sklearn.linear_model import LinearRegression

MODEL_PATH = "models/model.pkl"

@pytest.fixture(scope="module")
def load_model():
    """Фикстура для загрузки модели один раз для всех тестов"""
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

def test_model_file_exists():
    """Проверка, что файл модели существует"""
    assert os.path.exists(MODEL_PATH), f"Файл модели не найден: {MODEL_PATH}"

def test_model_type(load_model):
    """Проверка, что модель нужного класса"""
    assert isinstance(load_model, LinearRegression), "Модель не LinearRegression"

def test_model_coefficients_valid(load_model):
    """Проверка, что коэффициенты не пустые и не NaN"""
    coef = load_model.coef_
    assert coef is not None, "Коэффициенты модели отсутствуют"
    assert not np.isnan(coef).any(), "В коэффициентах есть NaN"
