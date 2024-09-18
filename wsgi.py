from celery import Celery
from flask import Flask
from config import CONFIG
from setup import create_dirs
from web import create_app

# create necessary directories
create_dirs()

contexts = create_app()
app: Flask = contexts[0]
celery: Celery = contexts[3]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)
