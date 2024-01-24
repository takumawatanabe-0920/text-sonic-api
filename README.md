# text-sonic-api

### set up

you need to set .env file

```
$ pip install --no-cache-dir --upgrade -r ./requirements.txt

$ uvicorn app.main.router:app --host 0.0.0.0 --port 8080 --reload --log-config=log_conf.yaml
```

### migration

```
$ pip install alembic

$ alembic init alembic # already done

<!-- generate sql file -->
$ alembic revision --autogenerate -m "Added scripts column"

<!-- exec migration -->
$ alembic upgrade head
```
