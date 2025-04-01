FROM python:3.9

WORKDIR /app

# Передаем build-аргументы для автоматизации сборки с значениями по умолчанию
ARG COMMIT_SHA=latest
ARG BRANCH_NAME=local

# Добавляем метаданные сборки
LABEL commit_sha=${COMMIT_SHA}
LABEL branch_name=${BRANCH_NAME}

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для Streamlit
EXPOSE 8501

# Запускаем Streamlit-приложение
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
