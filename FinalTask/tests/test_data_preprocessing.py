import os
import pandas as pd
import pytest

TRAIN_RAW = "data/train/train_data.csv"
TEST_RAW = "data/test/test_data.csv"
TRAIN_SCALED = "data/train/train_data_scaled.csv"
TEST_SCALED = "data/test/test_data_scaled.csv"

@pytest.fixture(scope="module")
def load_raw_data():
    return pd.read_csv(TRAIN_RAW), pd.read_csv(TEST_RAW)

@pytest.fixture(scope="module")
def load_scaled_data():
    return pd.read_csv(TRAIN_SCALED), pd.read_csv(TEST_SCALED)

def test_scaled_files_exist():
    assert os.path.exists(TRAIN_SCALED), f"{TRAIN_SCALED} отсутствует"
    assert os.path.exists(TEST_SCALED), f"{TEST_SCALED} отсутствует"

def test_shape_consistency(load_raw_data, load_scaled_data):
    df_train_raw, df_test_raw = load_raw_data
    df_train_scaled, df_test_scaled = load_scaled_data
    assert df_train_raw.shape == df_train_scaled.shape, "Формы train raw и scaled не совпадают"
    assert df_test_raw.shape == df_test_scaled.shape, "Формы test raw и scaled не совпадают"

def test_scaling_statistics(load_scaled_data):
    df_train_scaled, df_test_scaled = load_scaled_data
    for col in ['temp', 'humidity']:
        mean = df_train_scaled[col].mean()
        std = df_train_scaled[col].std()
        assert abs(mean) < 0.1, f"Среднее {col} в train далеко от 0: {mean}"
        assert 0.9 < std < 1.1, f"Стандартное отклонение {col} в train не около 1: {std}"

        mean_test = df_test_scaled[col].mean()
        std_test = df_test_scaled[col].std()
        # Для теста может не быть точно 0 и 1, но должно быть близко
        assert abs(mean_test) < 0.5, f"Среднее {col} в test далеко от 0: {mean_test}"
        assert std_test > 0, f"Стандартное отклонение {col} в test <= 0"
