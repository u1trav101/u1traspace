from flask import redirect, url_for
from flask.app import Flask
from flask_sock import Sock
from werkzeug import Response
from web.blueprints import auth_blueprint, blog_blueprint, message_blueprint, user_blueprint, conversation as _conversation
from web.decorators import validate_url_vars, require_auth, before_request as _before_request
import web.routes as routes


def declare_routes(app: Flask, sock: Sock) -> None:
    # registering blueprints
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    user_blueprint.register_blueprint(blog_blueprint, url_prefix="<user_id>/blog")
    app.register_blueprint(user_blueprint, url_prefix="/user")
    @sock.route("/<user_id>", message_blueprint)
    @validate_url_vars
    @require_auth
    def conversation(ws, user_id) -> Response | None:
        return _conversation(user_id, ws)
    app.register_blueprint(message_blueprint, url_prefix="/message")

    # defining function to be called before each request is processed
    @app.before_request
    def before_request() -> None:
        return _before_request()

    # registering all other miscellaneous routes
    @app.route("/preferences", methods=["GET", "POST"])
    @require_auth
    def preferences() -> Response | str:
        return routes.preferences()
    
    @app.route("/remove-friend/<user_id>", methods=["POST"])
    @require_auth
    @validate_url_vars
    def remove_friend(user_id: int) -> Response:
        return routes.remove_friend(user_id)

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
