import pytest
import app

@pytest.fixture
def datasets():
    return {
        "clean": app.generate_dataset(),
        "with_outliers": app.generate_dataset(outlier=True),
        "with_noise": app.generate_dataset(noise=True)
    }

@pytest.fixture
def trained_model(datasets):
    x_train, y_train = datasets["clean"]

    return app.train_model(x_train, y_train)

def test_clean_data_performance(trained_model, datasets):
    x_test, y_test = datasets["clean"]
    mse = app.evaluate_model(trained_model, x_test, y_test)

    assert mse < 5, f"MSE слишком высока для чистых данных (clean dataset): {mse}"

def test_outlier_data_performance(trained_model, datasets):
    x_test, y_test = datasets["with_outliers"]
    mse = app.evaluate_model(trained_model, x_test, y_test)

    assert mse < 10, f"MSE слишком высока для данных с выбросами (with_outliers dataset): {mse}"

def test_noisy_data_performance(trained_model, datasets):
    x_test, y_test = datasets["with_noise"]
    mse = app.evaluate_model(trained_model, x_test, y_test)

    assert mse > 5, "MSE неожиданно низкий для шумных данных (with_noise dataset). Должен быть высоким для обнаружения плохой производительности"
