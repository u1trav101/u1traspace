#! /bin/bash

source .venv/bin/activate
cd src
python setup.py
../.venv/bin/celery -A wsgi.celery worker