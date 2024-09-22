from celery import Celery
from flask import Flask
from flask_sock import Sock
from config import CONFIG
from setup import setup
from web import create_app
import log

log.write(
    "system",
    r"""booting...
                     ___                                             
               _   _/ | |_ _ __ __ _ ___ _ __   __ _  ___ ___            
              | | | | | __| '__/ _` / __| '_ \ / _` |/ __/ _ \           
              | |_| | | |_| | | (_| \__ \ |_) | (_| | (_|  __/           
     _____ ____\__,_|_|\__|_|  \__,_|___/ .__/ \__,_|\___\___|____ _____ 
    |_____|_____|                       |_|                 |_____|_____|
""",
)

setup()

contexts = create_app()
app: Flask = contexts[0]
sock: Sock = contexts[1]
celery: Celery = contexts[2]

log.write("wsgi", "serving requests...")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)
