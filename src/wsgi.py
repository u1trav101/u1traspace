from celery import Celery
from flask import Flask
from flask_caching import Cache
from flask_sock import Sock
from config import CONFIG
from setup import setup
from web import create_app

setup()

contexts = create_app()
app: Flask = contexts[0]
sock: Sock = contexts[1]
cache: Cache = contexts[2]
celery: Celery = contexts[3]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)
