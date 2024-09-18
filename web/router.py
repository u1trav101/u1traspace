from flask import redirect, url_for
from flask.app import Flask
from werkzeug import Response
from web.decorators import (
    require_auth,
)
import web.routes as routes


def router(app: Flask) -> Flask:
    # defining redirects
    @app.route("/users/")
    def users_redirect() -> Response:
        return redirect(url_for("user.browse"))

    @app.route("/posts/")
    def posts_redirect() -> Response:
        return redirect(url_for("news"))

    # registering all other miscellaneous routes
    @app.route("/preferences", methods=["GET", "POST"])
    @require_auth
    def preferences() -> Response | str:
        return routes.preferences()

    @app.route("/")
    def index() -> str:
        return routes.index()

    @app.route("/set-timezone", methods=["POST"])
    def set_timezone() -> str:
        return routes.set_timezone()

    @app.route("/news")
    def news() -> Response | str:
        return routes.news()

    @app.route("/search", methods=["GET", "POST"])
    def search() -> Response | str | tuple:
        return routes.search()

    @app.route("/konata")
    def konata() -> Response:
        return routes.konata()

    @app.route("/rss/<request>")
    def rss(request: str) -> Response | str | tuple:
        return routes.rss(request)

    @app.route("/rules")
    def rules() -> str:
        return routes.rules()

    return app
