from flask import Flask
from flask_cors import CORS
from flask_limiter.util import get_remote_address
from flask_sock import Sock
from flask_limiter import Limiter
from werkzeug.middleware.proxy_fix import ProxyFix
from markdown import markdown
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

# instialising wsgi app instance
app: Flask = Flask("u1traspace")

# applying configs from config class
app.config.from_object(CONFIG)

# fixing rate_limiter key_func if in prod (deployed behind reverse proxy)
if not CONFIG.DEBUG:
    ProxyFix(app.wsgi_app, x_for=CONFIG.NUM_OF_PROXIES)

# initialising flask extensions
CORS(app)
sock = Sock(app)
Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=CONFIG.REDIS_BROKER_URL,
    default_limits=["3 per second"]
)

celery: Celery = celery_init_app(app)

# declaring jinja filters
app.add_template_filter(regex_replace)
app.add_template_filter(markdown)

# declaring the app URL endpoints
declare_routes(app, sock)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)
