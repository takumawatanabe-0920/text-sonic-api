#!/bin/bash

# Alembicマイグレーションを実行
alembic upgrade head

# FastAPIアプリケーションを起動
exec uvicorn app.main.router:app --host 0.0.0.0 --port 8080 --reload --log-config=log_conf.yaml