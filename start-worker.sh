#! /bin/bash

source .venv/bin/activate
.venv/bin/celery -A wsgi.celery worker