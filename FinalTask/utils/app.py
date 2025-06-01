import os
import sys
import streamlit as st

# Чтобы гарантированно подтягивался utils/model.py
if __name__ == "__main__":
    sys.path.append(os.getcwd())

from utils.model import train_model, predict_temperature

st.set_page_config(
    page_title="Прогноз температуры",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("🌡️ Прогноз температуры на основе ML")
st.write(
    """
    Это приложение использует предобученную модель.
    Введите номер дня и уровень влажности, чтобы увидеть прогноз температуры.
    """
)

# Поля ввода
input_day = st.number_input(
    label="Номер дня (целое число ≥ 0)",
    min_value=0,
    value=15,
    step=1
)
input_humidity = st.number_input(
    label="Уровень влажности (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=0.1
)

# Загружаем модель и скейлеры (никакого переобучения не будет)
with st.spinner("Загружаем предобученную модель..."):
    try:
        model, scaler_humidity, scaler_temp = train_model()
        st.success("Модель успешно загружена!")
    except Exception as e:
        st.error(f"Не удалось загрузить модель: {e}")
        st.stop()

# При клике по кнопке делаем предсказание
if st.button("Сделать прогноз"):
    try:
        pred = predict_temperature(
            model,
            scaler_humidity,
            scaler_temp,
            int(input_day),
            float(input_humidity)
        )
        
        # Если predict_temperature вдруг вернула None — обрабатываем отдельно
        if pred is None:
            st.error("Не удалось получить прогноз (функция вернула None).")
        else:
            # Убедимся, что pred — число, и применим форматирование
            try:
                formatted = f"{pred:.2f}"
            except Exception:
                # Если даже форматирование не сработало, просто выводим raw-значение
                formatted = str(pred)
            st.write(f"## 🔵 Предсказанная температура: **{formatted} °C**")

    except Exception as e:
        st.error(f"Ошибка при предсказании: {e}")
