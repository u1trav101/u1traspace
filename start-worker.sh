#! /bin/bash

source .venv/bin/activate
python setup.py
.venv/bin/celery -A wsgi.celery worker