#!/bin/bash
# Скрипт для автоматизированной сборки, деплоя и запуска Docker-образа

set -e

# Получаем текущий SHA коммита и имя ветки
COMMIT_SHA=$(git rev-parse --short HEAD)
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

echo "Building image with COMMIT_SHA=${COMMIT_SHA} and BRANCH_NAME=${BRANCH_NAME}"

# Экспортируем переменные для docker-compose
export COMMIT_SHA
export BRANCH_NAME

# Собираем Docker образ с помощью docker-compose
docker-compose build

# Тегируем образ как latest
docker tag shoolife/streamlit_app:${COMMIT_SHA} shoolife/streamlit_app:latest

# Отправляем образы в Docker Hub
docker push shoolife/streamlit_app:${COMMIT_SHA}
docker push shoolife/streamlit_app:latest

# Запускаем контейнер в фоновом режиме
docker-compose up -d

echo "Контейнер запущен. Приложение доступно по адресу http://localhost:8501"
