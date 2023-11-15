FROM python:3.10-slim
ENV NODE_ENV=production
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app
COPY . /code

# エントリーポイントスクリプトをコピー
COPY start.sh ./
RUN chmod +x ./start.sh

# アプリケーションを起動
CMD ["./start.sh"]