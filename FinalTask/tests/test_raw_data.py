import pandas as pd
import pytest

ALLOWED_CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
]

# Тесты для тренировочных данных
def test_raw_train_data():
    df = pd.read_csv("FinalTask/data/train/train_data.csv")

    assert not df.isnull().values.any(), "Есть пропуски в данных"
    assert pd.api.types.is_integer_dtype(df['day']), "Колонка 'day' не целочисленная"
    assert pd.api.types.is_float_dtype(df['temp']), "Колонка 'temp' не числовая"
    assert pd.api.types.is_float_dtype(df['humidity']), "Колонка 'humidity' не числовая"
    assert df['city'].dtype == object, "Колонка 'city' не строкового типа"
    assert df['temp'].between(-50, 50).all(), "Есть температуры вне ожидаемого диапазона"
    assert df['humidity'].between(0, 100).all(), "Есть значения влажности вне диапазона 0-100%"
    assert set(df['city']).issubset(set(ALLOWED_CITIES)), "Есть недопустимые города в данных"
    expected_days = list(range(len(df)))
    assert list(df['day']) == expected_days, "Колонка 'day' не последовательна"

    # Проверка температурных выбросов
    Q1 = df['temp'].quantile(0.25)
    Q3 = df['temp'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['temp'] < Q1 - 1.5*IQR) | (df['temp'] > Q3 + 1.5*IQR)]

    if not outliers.empty:
        print(f"Внимание! Обнаружено {len(outliers)} выбросов температуры в тренировочных данных. Это ожидаемо для текущих данных.")
    else:
        print("Выбросы температуры не обнаружены.")

    # Проверка среднего значения температуры
    mean_temp = df['temp'].mean()
    assert 5 < mean_temp < 15, f"Средняя температура ({mean_temp}) вне нормы"

    # Проверка на дубликаты
    assert not df.duplicated().any(), "Есть дубликаты строк"

    # Проверка порядка и целостности дней
    days = df['day']
    assert days.is_monotonic_increasing, "Дни не упорядочены"
    assert days.is_unique, "Дни повторяются"
    expected_days = set(range(len(df)))
    assert set(days) == expected_days, "Неполный набор дней"

    # Проверка распределения городов
    city_counts = df['city'].value_counts(normalize=True)
    assert all(city_counts < 0.6), "Один город занимает слишком большую долю"

    print("Тесты для тренировочных данных прошли успешно.")

# Тесты для тестовых данных    
def test_raw_test_data():
    df = pd.read_csv("FinalTask/data/test/test_data.csv")

    assert not df.isnull().values.any(), "Есть пропуски в тестовых данных"
    assert pd.api.types.is_integer_dtype(df['day']), "Колонка 'day' не целочисленная в тестовых данных"
    assert pd.api.types.is_float_dtype(df['temp']), "Колонка 'temp' не числовая в тестовых данных"
    assert pd.api.types.is_float_dtype(df['humidity']), "Колонка 'humidity' не числовая в тестовых данных"
    assert df['city'].dtype == object, "Колонка 'city' не строкового типа в тестовых данных"
    assert df['temp'].between(-50, 50).all(), "Есть температуры вне ожидаемого диапазона в тестовых данных"
    assert df['humidity'].between(0, 100).all(), "Есть значения влажности вне диапазона 0-100% в тестовых данных"
    assert set(df['city']).issubset(set(ALLOWED_CITIES)), "Есть недопустимые города в тестовых данных"
    expected_days = list(range(len(df)))
    assert list(df['day']) == expected_days, "Колонка 'day' не последовательна в тестовых данных"

    # Проверка температурных выбросов
    Q1 = df['temp'].quantile(0.25)
    Q3 = df['temp'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['temp'] < Q1 - 1.5*IQR) | (df['temp'] > Q3 + 1.5*IQR)]

    if not outliers.empty:
        print(f"Внимание! Обнаружено {len(outliers)} выбросов температуры в тестовых данных. Это ожидаемо для текущих данных.")
    else:
        print("Выбросы температуры не обнаружены.")

    # Проверка среднего значения температуры
    mean_temp = df['temp'].mean()
    assert 5 < mean_temp < 15, f"Средняя температура ({mean_temp}) вне нормы"

    # Проверка на дубликаты
    assert not df.duplicated().any(), "Есть дубликаты строк"

    # Проверка порядка и целостности дней
    days = df['day']
    assert days.is_monotonic_increasing, "Дни не упорядочены"
    assert days.is_unique, "Дни повторяются"
    expected_days = set(range(len(df)))
    assert set(days) == expected_days, "Неполный набор дней"

    # Проверка распределения городов
    city_counts = df['city'].value_counts(normalize=True)
    assert all(city_counts < 0.6), "Один город занимает слишком большую долю"

    print("Тесты для тестовых данных прошли успешно.")
