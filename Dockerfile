FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY data/ ./data
COPY models/ ./models
COPY pipline.sh pipline.sh

ENTRYPOINT ["bash", "pipline.sh"]
