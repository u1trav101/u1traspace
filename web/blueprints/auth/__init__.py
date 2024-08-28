from flask import Blueprint
from werkzeug import Response
from web.blueprints.auth.login import _login
from web.blueprints.auth.logout import _logout
from web.blueprints.auth.register import _register
from web.decorators import require_auth, reject_auth


auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/login", methods=["GET", "POST"])
@reject_auth
def login() -> Response | str:
    return _login()

@auth_blueprint.route("/logout")
@require_auth
def logout() -> Response:
    return _logout()

@auth_blueprint.route("/register", methods=["GET", "POST"])
@reject_auth
def register() -> Response | str:
    return _register()