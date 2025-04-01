FROM python:3.9

WORKDIR /app

ARG COMMIT_SHA=latest
ARG BRANCH_NAME=local

LABEL commit_sha=${COMMIT_SHA}
LABEL branch_name=${BRANCH_NAME}

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
