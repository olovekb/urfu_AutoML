import streamlit as st
from utils.model import train_model, predict_temperature

st.title("Прогнозирование температуры")
st.write("Введите данные для прогноза:")

# Ввод дня и влажности
input_day = st.number_input("День (номер дня)", min_value=0, value=15, step=1)
input_humidity = st.number_input("Влажность (%)", min_value=0.0, max_value=100.0, value=50.0)

# Обучение модели при старте приложения
with st.spinner("Обучение модели..."):
    try:
        model, scaler_humidity, scaler_temp = train_model()
    except Exception as e:
        st.error(f"Ошибка при обучении модели: {e}")
        st.stop()

if st.button("Сделать предсказание"):
    prediction = predict_temperature(model, scaler_humidity, scaler_temp, input_day, input_humidity)
    st.success(f"Предсказанная температура: {prediction:.2f}")
