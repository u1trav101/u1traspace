from flask import Flask
from flask_cors import CORS
from flask_misaka import Misaka
from celery import Celery
from tasks import celery_init_app
from web import declare_routes, regex_replace
from config import CONFIG
import os


# create necessary directories
os.makedirs(os.path.dirname("./.tmp/img"), exist_ok=True)
os.makedirs(os.path.dirname("./.tmp/audio"), exist_ok=True)
os.makedirs(os.path.dirname("./usercontent/img/raw"), exist_ok=True)
os.makedirs(os.path.dirname("./usercontent/img/rsz/200px"), exist_ok=True)
os.makedirs(os.path.dirname("./usercontent/img/rsz/100px"), exist_ok=True)
os.makedirs(os.path.dirname("./usercontent/img/rsz/32px"), exist_ok=True)
os.makedirs(os.path.dirname("./usercontent/audio"), exist_ok=True)
os.makedirs(os.path.dirname("./usercontent/css"), exist_ok=True)

app: Flask = Flask("u1traspace")

# applying configs from config class
app.config.from_object(CONFIG)

# initialising flask extensions
CORS(app)
Misaka(app, autolink=True)

celery: Celery = celery_init_app(app)

# declaring jinja filters
app.add_template_filter(regex_replace)

# declaring the app URL endpoints
declare_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)
