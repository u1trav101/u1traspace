from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter.util import get_remote_address
from flask_sock import Sock
from flask_limiter import Limiter
from werkzeug.middleware.proxy_fix import ProxyFix
from markdown import markdown
from celery import Celery
from tasks import celery_init_app
from config import CONFIG
from web.formatting import regex_replace
from web.router import router
from web.blueprints import (
    AuthBlueprint,
    UserBlueprint,
    BlogBlueprint,
    FriendsBlueprint,
    MessagesBlueprint,
)
from web.decorators import (
    before_request as _before_request,
)
import log


def create_app():
    log.write(__name__, "building application...")

    # instialising wsgi app instance
    app: Flask = Flask("u1traspace", static_url_path="")

    # applying configs from config class
    app.config.from_object(CONFIG)

    # fixing rate_limiter key_func if in prod (deployed behind reverse proxy)
    if not CONFIG.DEBUG:
        ProxyFix(app.wsgi_app, x_for=CONFIG.NUM_OF_PROXIES)

    # initialising flask extensions
    CORS(app)
    sock = Sock(app)
    cache = Cache(app)
    Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=CONFIG.REDIS_BROKER_URL,
        default_limits=["3 per second"],
    )

    celery: Celery = celery_init_app(app)

    # declaring jinja filters
    app.add_template_filter(regex_replace)
    app.add_template_filter(markdown)

    # building blueprints
    auth_blueprint = AuthBlueprint(cache).get_blueprint()
    user_blueprint = UserBlueprint().get_blueprint()
    blog_blueprint = BlogBlueprint(cache).get_blueprint()
    friends_blueprint = FriendsBlueprint().get_blueprint()
    messages_blueprint = MessagesBlueprint(sock).get_blueprint()

    user_blueprint.register_blueprint(blog_blueprint, url_prefix="<user_id>/blog")
    user_blueprint.register_blueprint(friends_blueprint, url_prefix="<user_id>/friends")

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(messages_blueprint, url_prefix="/messages")

    @app.before_request
    def before_request() -> None:
        return _before_request()

    app = router(app, cache)
    app.app_context().push()

    log.write(__name__, "building application... DONE")

    return app, sock, cache, celery
