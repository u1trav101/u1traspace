from flask import redirect, url_for
from flask.app import Flask
from flask_caching import Cache
from werkzeug import Response
from config.config import CONFIG
from web.decorators import (
    require_auth,
)
import web.routes as routes
from web.utils import method_is_post


def router(app: Flask, cache: Cache) -> Flask:
    # defining redirects
    @app.route("/users/")
    @cache.cached(CONFIG.CACHE_EXT_TIMEOUT)
    def users_redirect() -> Response:
        return redirect(url_for("user.browse"))

    @app.route("/posts/")
    @cache.cached(CONFIG.CACHE_EXT_TIMEOUT)
    def posts_redirect() -> Response:
        return redirect(url_for("news"))

    # registering all other miscellaneous routes
    @app.route("/preferences", methods=["GET", "POST"])
    @require_auth
    def preferences() -> Response | str:
        return routes.preferences()

    @app.route("/")
    @cache.cached(CONFIG.CACHE_EXT_TIMEOUT)
    def index() -> str:
        return routes.index()

    @app.route("/set-timezone", methods=["POST"])
    def set_timezone() -> str:
        return routes.set_timezone()

    @app.route("/news")
    @cache.cached(timeout=CONFIG.CACHE_DEFAULT_TIMEOUT)
    def news() -> Response | str:
        return routes.news()

    @app.route("/search", methods=["GET", "POST"])
    @cache.cached(timeout=CONFIG.CACHE_EXT_TIMEOUT, unless=method_is_post)
    def search() -> Response | str | tuple:
        return routes.search()

    @app.route("/konata")
    @cache.cached(timeout=CONFIG.CACHE_EXT_TIMEOUT)
    def konata() -> Response:
        return routes.konata()

    @app.route("/rss/<request>")
    @cache.memoize(timeout=CONFIG.CACHE_DEFAULT_TIMEOUT)
    def rss(request: str) -> Response | str | tuple:
        return routes.rss(request)

    @app.route("/rules")
    @cache.cached(CONFIG.CACHE_EXT_TIMEOUT)
    def rules() -> str:
        return routes.rules()

    return app
