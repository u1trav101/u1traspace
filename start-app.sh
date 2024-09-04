#! /bin/sh

.venv/bin/gunicorn --pythonpath .venv/bin/python --workers 4 --bind 0.0.0.0:5003 wsgi:app