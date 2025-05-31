#!/bin/bash

echo "Running data creation..."
python3 src/data_creation.py

echo "Running data preprocessing..."
python3 src/data_preprocessing.py

echo "Running model training..."
python3 src/model_preparation.py

echo "Running model testing..."
python3 src/model_testing.py
