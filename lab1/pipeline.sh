#!/bin/bash
# Убедитесь, что скрипт исполняется из директории lab1

# При необходимости можно установить требуемые библиотеки, например:
# pip install -r requirements.txt

echo "Running data creation..."
python3 data_creation.py

echo "Running data preprocessing..."
python3 data_preprocessing.py

echo "Running model training..."
python3 model_preparation.py

echo "Running model testing..."
python3 model_testing.py
