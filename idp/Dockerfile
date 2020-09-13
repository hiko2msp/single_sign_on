FROM python:3.8-alpine

WORKDIR /app

ADD requirements.txt .
# コンテナ内で必要なパッケージをインストール
RUN apk add --no-cache build-base mariadb-connector-c-dev
# requirements.txtにリストされたPythonパッケージをインストールする
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

ADD main.py .
ARG PORT
ENV PORT ${PORT}
run echo uvicorn main:app --reload --host 0.0.0.0 --port ${PORT}
# FastAPIを8000ポートで待機
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", ${PORT}]
CMD uvicorn main:app --reload --host 0.0.0.0 --port ${PORT}
