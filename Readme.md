# **Final Task**

# Прогноз температуры с помощью линейной регрессии

Это репозиторий демонстрирует полный цикл создания, предобработки и моделирования синтетических данных для прогнозирования температуры на основе простого алгоритма линейной регрессии. Проект включает:

- Генерацию синтетических данных (температура, влажность, город, день);
- Предобработку (масштабирование) данных;
- Обучение модели линейной регрессии и сохранение её вместе со скейлерами;
- Тестирование качества модели на отложенной выборке;
- Веб-приложение на Streamlit для интерактивного прогноза температуры;
- Dockerfile для контейнеризации веб-приложения;
- Jenkinsfile и `pipline.sh` для автоматизации CI/CD с DVC и Jenkins;
- Комплект тестов на pytest для проверки корректности данных и работоспособности моделей.

---

## Содержание репозитория

```
├── data/
│   ├── train/
│   │   ├── train_data.csv            ← Исходный тренировочный датасет (генерируется автоматически)
│   │   └── train_data_scaled.csv     ← Масштабированный тренировочный датасет (после data_preprocessing.py)
│   └── test/
│       ├── test_data.csv             ← Исходный тестовый датасет (генерируется автоматически)
│       └── test_data_scaled.csv      ← Масштабированный тестовый датасет (после data_preprocessing.py)
│
├── models/
│   └── model.pkl                     ← Сериализованный кортеж (model, scaler_temp, scaler_humidity)
│
├── src/
│   ├── data_creation.py              ← Генерация синтетических «сырых» данных
│   ├── data_preprocessing.py         ← Масштабирование признаков (temp, humidity)
│   ├── model_preparation.py          ← Обучение LinearRegression и сохранение модели
│   └── model_testing.py              ← Загрузка модели и оценка качества на тестовом наборе
│
├── utils/
│   ├── app.py                        ← Streamlit-приложение для интерактивного прогноза
│   └── model.py                      ← Функции-обёртки: train_model() и predict_temperature()
│
├── tests/
│   ├── test_raw_data.py              ← Проверка исходных CSV (dtype, диапазоны, распределение городов)
│   ├── test_data_preprocessing.py    ← Проверка статистик (mean≈0, std≈1) после масштабирования
│   ├── test_model_preparation.py     ← Проверка корректности сохранённой модели (LinearRegression и непустые коэффициенты)
│   └── test_model_testing.py         ← Проверка, что MSE ≥ 0 и R² ∈ [−1, 1] на тестовых данных
│
├── .dvc/
│   └── …                              ← Конфигурация DVC и локальный кэш для версионирования данных
│
├── .gitignore
├── Dockerfile                        ← Инструкции для сборки Docker-образа Streamlit-приложения
├── Jenkinsfile                       ← Конфигурация CI/CD-пайплайна для Jenkins с DVC
├── pipline.sh                        ← Простой bash-скрипт для последовательного запуска всех этапов
├── requirements.txt                  ← Перечень зависимостей Python (включая streamlit, sklearn и др.)
└── README.md                         ← Этот файл
```

---

## Описание проекта

Алгоритм работы:

1. **Генерация данных (src/data_creation.py)**
   - Создаются две папки: `data/train/` и `data/test/`.
   - Для каждой папки генерируется CSV-файл с 100 точками данных (100 дней) по 4 признакам:
     - `day` — номер дня (целое от 0 до 99);
     - `temp` — «температура» (синусоидальная функция + шум + выбросы в тренировочном наборе);
     - `humidity` — случайная влажность (равномерно от 30 до 90);
     - `city` — случайный выбор из 10 городов (New York, Los Angeles, Chicago, Houston, Phoenix, Philadelphia, San Antonio, San Diego, Dallas, San Jose).
   - Генерация происходит с помощью NumPy и pandas и сохраняет файлы:
     ```
     data/train/train_data.csv
     data/test/test_data.csv
     ```

2. **Предобработка данных (src/data_preprocessing.py)**
   - Читает `data/train/train_data.csv` и `data/test/test_data.csv`.
   - Создаёт `StandardScaler` для `temp` и для `humidity`, обучая их на тренировочных данных.
   - Применяет `fit_transform` к столбцам `temp` и `humidity` тренировочного набора, а затем `transform` к тем же столбцам тестового набора.
   - Сохраняет масштабированные версии в:
     ```
     data/train/train_data_scaled.csv
     data/test/test_data_scaled.csv
     ```
   - Проверяет существование нужных директорий (`data/train`, `data/test`) и создаёт их при необходимости.

3. **Обучение модели (src/model_preparation.py)**
   - Читает `data/train/train_data_scaled.csv`.
   - Формирует матрицу признаков `X_train` из:
     - `sin_day` = sin(2π⋅day/30)
     - `cos_day` = cos(2π⋅day/30)
     - `humidity` (значение уже масштабировано)
   - Целевая переменная `y_train` — это масштабированное значение `temp`.
   - Обучает `LinearRegression` на этих данных.
   - Затем повторно читает «сырые» данные `data/train/train_data.csv`, чтобы обучить два скейлера:
     - `scaler_temp` (обучается на столбце `temp` из сырых данных),
     - `scaler_humidity` (на столбце `humidity`).
   - Сохраняет в директорию `models/` файл `model.pkl`, который содержит кортеж `(model, scaler_temp, scaler_humidity)`.

4. **Тестирование модели (src/model_testing.py)**
   - Читает `data/test/test_data_scaled.csv`.
   - Формирует `X_test` из тех же признаков (`sin_day`, `cos_day`, `humidity`), а `y_test` — то, что лежит в столбце `temp` в масштабированных тестовых данных.
   - Загружает сериализованный кортеж `(model, scaler_temp, scaler_humidity)` из `models/model.pkl`.
   - Выполняет предсказание `y_pred = model.predict(X_test)`.
   - Считает метрики качества:
     - `Mean Squared Error (MSE)`
     - `R² Score`
   - Печатает результаты в консоль.

5. **Веб-приложение на Streamlit (utils/app.py + utils/model.py)**
   - Файл `utils/model.py` содержит две функции:
     - `train_model()` — проверяет наличие `models/model.pkl`, загружает из него кортеж `(model, scaler_temp, scaler_humidity)` и возвращает `(model, scaler_humidity, scaler_temp)` (именно в таком порядке, чтобы `app.py` корректно распаковал).
     - `predict_temperature(model, scaler_humidity, scaler_temp, input_day, input_humidity)` —
       1. Масштабирует входную влажность через `scaler_humidity`.
       2. Вычисляет `sin_day, cos_day` по переданному `input_day`.
       3. Формирует DataFrame с тремя признаками и вызывает `model.predict(…)`, получая `pred_scaled`.
       4. Выполняет обратное масштабирование `pred_scaled` через `scaler_temp.inverse_transform(…)`, возвращая реальное значение температуры в градусах.
   - В файле `utils/app.py` реализована страница Streamlit:
     1. При старте загружается модель и скейлеры через `train_model()`.
     2. Пользователь вводит в боковой панели (`st.sidebar`) номер дня (целое) и влажность (число).
     3. При нажатии на кнопку запускается `predict_temperature(…)`, результат выводится на страницу.
     4. Обрабатываются возможные ошибки (файл модели отсутствует, некорректный ввод и т. д.).

6. **Dockerfile**
   - Базируется на `python:3.10-slim`.
   - Устанавливает `dos2unix` для конвертации возможных CRLF в LF.
   - Копирует `requirements.txt` и устанавливает зависимости (фильтруя `pywin32` при необходимости).
   - Копирует подготовленную модель из `models/` и код веб-приложения из `utils/`.
   - Пробрасывает порт `8501`, на котором по умолчанию слушает Streamlit.
   - `ENTRYPOINT`: `streamlit run utils/app.py --server.port=8501 --server.address=0.0.0.0`.

7. **Jenkinsfile**
   Пайплайн CI/CD, описанный для Jenkins:
   - **Checkout** — клонирование репозитория.
   - **Setup Python & DVC** — установка Python, DVC, настройка виртуального окружения.
   - **DVC Pull Data** — получение «сырых» данных из удалённого DVC-хранилища (параметр `DVC_REMOTE = storage`).
   - **Generate & Track Raw Data** — (при необходимости) запуск `src/data_creation.py`, добавление результата в DVC.
   - **Preprocess & Track Processed Data** — запуск `src/data_preprocessing.py`, `dvc add` для масштабированных данных.
   - **Train & Save Model** — запуск `src/model_preparation.py`, добавление `models/model.pkl` в DVC.
   - **Unit & Data Tests** — запуск `pytest`, отчёт в формате JUnit.
   - **Push Data to Remote** — пуш DVC-данных в удалённый `storage`.
   - **Docker Login** — логин в Docker Registry.
   - **Build & Push Docker Image** — сборка Docker-образа и пуш в Docker Hub под именем `shoolife/urfu-automl-app`.

8. **Пакет `pipline.sh`**
   Простой bash-скрипт, который последовательно запускает:
   ```bash
   python3 src/data_creation.py
   python3 src/data_preprocessing.py
   python3 src/model_preparation.py
   python3 src/model_testing.py
   ```
   После выполнения скрипта в папках `data/` и `models/` оказываются все необходимые файлы:
   - `data/train/train_data.csv`
   - `data/test/test_data.csv`
   - `data/train/train_data_scaled.csv`
   - `data/test/test_data_scaled.csv`
   - `models/model.pkl`
   - В консоли результаты тестирования модели (MSE, R²).

9. **Тесты (pytest)**
   - `tests/test_raw_data.py`
     Проверяет, что в `data/train/train_data.csv` и `data/test/test_data.csv` нет пропусков, столбцы имеют правильные типы (`day` — int, `temp` — float, `humidity` — float, `city` — string), температура лежит в диапазоне [−50, 50], а дни образуют полный набор `0…N−1`. Также проверяет, что ни один город не занимает более 60% сэмплов.
   - `tests/test_data_preprocessing.py`
     Проверяет, что после масштабирования в тренировочном наборе среднее `temp` и `humidity` близко к 0, а стандартное отклонение ≈ 1 (`0.9 < std < 1.1`). В тестовом наборе проверяет, что `mean` < 0.5, `std > 0`.
   - `tests/test_model_preparation.py`
     Проверяет, что файл `models/model.pkl` существует и его первый элемент — объект `LinearRegression`, а коэффициенты (`coef_`) не пустые и не содержат NaN.
   - `tests/test_model_testing.py`
     Загружает модель, читает `data/test/test_data_scaled.csv`, считает MSE >= 0 и R² ∈ [−1, 1].

#### Запуск образа после публикации в Docker Hub

После того как вы запушили образ в Docker Hub, его можно запустить следующим образом:

```bash
docker pull shoolife/urfu-automl-app:27
docker run -p 8501:8501 shoolife/urfu-automl-app:27