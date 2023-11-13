# text-sonic-api

### set up

you need to set .env file

```
$ pip install --no-cache-dir --upgrade -r ./requirements.txt

$ uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload
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
