#!/bin/bash

env_bin=/www/server/pyporject_evn/bee2c6e1ee17c225fec353492bd9078b_venv/bin

sudo ${env_bin}/pip install -r requirements.txt
${env_bin}/python3 manage.py makemigrations

sudo chown ubuntu:ubuntu db.sqlite3

${env_bin}/python3 manage.py migrate
${env_bin}/python3 manage.py collectstatic

# /www/server/pyporject_evn/94d7bd8179533c59aca987c718472328_venv/bin/python3 manage.py makemigrations
# /www/server/pyporject_evn/94d7bd8179533c59aca987c718472328_venv/bin/python3 manage.py migrate
# /www/server/pyporject_evn/94d7bd8179533c59aca987c718472328_venv/bin/python3 manage.py collectstatic

# nohup /www/server/pyporject_evn/bee2c6e1ee17c225fec353492bd9078b_venv/bin/python3 manage.py runserver 0.0.0.0:8200 &
