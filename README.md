# text-sonic-api

server 側のセットアップ

server ディレクトリ配下に.env を用意する必要があります。

```
$ pip install --no-cache-dir --upgrade -r ./requirements.txt

$ uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload
```
