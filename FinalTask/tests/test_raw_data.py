import warnings
import pandas as pd
import pytest

ALLOWED_CITIES = {
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
}

def check_dataframe(df, name):
    assert not df.isnull().values.any(), "Есть пропуски"
    assert pd.api.types.is_integer_dtype(df['day']), "'day' не int"
    assert pd.api.types.is_float_dtype(df['temp']), "'temp' не float"
    assert pd.api.types.is_float_dtype(df['humidity']), "'humidity' не float"
    assert df['city'].dtype == object, "'city' не строка"
    assert df['temp'].between(-50, 50).all(), "Температура вне диапазона"
    assert df['humidity'].between(0, 100).all(), "Влажность вне диапазона"
    assert set(df['city']).issubset(ALLOWED_CITIES), "Недопустимые города"
    assert list(df['day']) == list(range(len(df))), "'day' не последовательна"

    Q1, Q3 = df['temp'].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    outliers = df[(df['temp'] < Q1 - 1.5*IQR) | (df['temp'] > Q3 + 1.5*IQR)]

    if not outliers.empty:
        warn_msg = "Внимание! Выбросы температуры:\n" + outliers.to_string(index=True)
        warnings.warn(warn_msg, UserWarning)

    mean_temp = df['temp'].mean()
    assert 5 < mean_temp < 15, f"Средняя температура ({mean_temp}) вне нормы"

    assert not df.duplicated().any(), "Есть дубликаты"
    assert df['day'].is_monotonic_increasing, "'day' не упорядочен"
    assert df['day'].is_unique, "'day' не уникален"
    assert set(df['day']) == set(range(len(df))), "Неполный набор дней"

    city_counts = df['city'].value_counts(normalize=True)
    assert all(city_counts < 0.6), "Один город занимает слишком большую долю"

    print(f"Тесты для данных '{name}' прошли успешно.")

@pytest.mark.parametrize("filepath, name", [
    ("data/train/train_data.csv", "train_data.csv"),
    ("data/test/test_data.csv", "test_data.csv"),
])
def test_raw_data(filepath, name):
    df = pd.read_csv(filepath)
    check_dataframe(df, name)
