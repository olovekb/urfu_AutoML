import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def generate_dataset(noise=False, outlier=False):
    xs = np.linspace(0, 10, 100).reshape(-1, 1)
    ys = xs.flatten() + np.random.random(100) * 2 - 1

    if outlier:
        ys[25:45] *= 2
    if noise:
        ys += np.random.normal(0, 3, 100)

    return xs, ys

def train_model(x_train, y_train):
    return LinearRegression().fit(x_train, y_train)

def evaluate_model(model, x_test, y_test):
    return mean_squared_error(y_test, model.predict(x_test))
