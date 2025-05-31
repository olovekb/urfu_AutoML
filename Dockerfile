# 1. Базовый образ
FROM python:3.10-slim

# 2. Рабочая директория внутри контейнера
WORKDIR /app

# 3. Устанавливаем dos2unix — чтобы на этапе сборки конвертировать CRLF → LF
RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*

# 4. Копируем только requirements.txt и ставим зависимости
COPY requirements.txt ./
RUN grep -vE '^pywin32==' requirements.txt > /tmp/requirements_unix.txt \
    && pip install --no-cache-dir -r /tmp/requirements_unix.txt

# 5. Копируем исходники и данные в контейнер
COPY src/ ./src
COPY data/ ./data
COPY models/ ./models
COPY pipeline.sh ./pipeline.sh

# 6. Конвертируем все .sh и .py в LF-формат (удаляем возможные `\r` в конце каждой строки)
#    и делаем pipeline.sh исполняемым
RUN find /app -type f \( -name "*.sh" -o -name "*.py" \) -exec dos2unix {} \; \
    && chmod +x /app/pipeline.sh

# 7. Указываем точку входа — запуск вашего пайплайна
ENTRYPOINT ["bash", "pipeline.sh"]
