FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN grep -vE '^pywin32==' requirements.txt > /tmp/reqs.txt \
 && pip install --no-cache-dir -r /tmp/reqs.txt

COPY src/ ./src
COPY data/ ./data
COPY models/ ./models
COPY pipline.sh pipline.sh

ENTRYPOINT ["bash", "pipline.sh"]
