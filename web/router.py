from flask.app import Flask
from flask_sock import Sock
from werkzeug import Response
from web.blueprints import auth_blueprint, blog_blueprint, message_blueprint, user_blueprint, conversation as _conversation
import web.misc as misc
import web.routes as routes


def declare_routes(app: Flask, sock: Sock) -> None:
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    
    user_blueprint.register_blueprint(blog_blueprint, url_prefix="<user_id>/blog")
    
    app.register_blueprint(user_blueprint, url_prefix="/user")
    
    @sock.route("/<user_id>", message_blueprint)
    @misc.validate_url_vars
    def conversation(ws, user_id) -> Response | None:
        return _conversation(user_id, ws)
    app.register_blueprint(message_blueprint, url_prefix="/msg")

    @app.before_request
    def before_request() -> None:
        return misc.before_request()

    @app.route("/")
    def index() -> str:
        return routes.index()
    
    @app.route("/set-timezone", methods=["POST"])
    def set_timezone() -> str:
        return routes.set_timezone()
    
    @app.route("/users/")
    def user_list() -> Response | str:
        return routes.user_list()
    
    @app.route("/news")
    def news() -> Response | str:
        return routes.news()

    @app.route("/preferences/", methods=["GET", "POST"])
    def preferences() -> Response | str:
        return routes.preferences()

    @app.route("/notifications/", methods=["GET", "POST"])
    def notifications() -> Response | str:
        return routes.notifications()

    @app.route("/search/", methods=["GET", "POST"])
    def search() -> str | tuple:
        return routes.search()

    @app.route("/konata/")
    def konata() -> Response:
        return routes.konata()
    
    @app.route("/rss/<request>")
    def rss(request: str) -> Response | str | tuple:
        return routes.rss(request)
    
    @app.route("/faq/")
    def faq() -> str:
        return routes.faq()
