from flask import Blueprint
from werkzeug import Response
from web.blueprints.auth.login import login as _login
from web.blueprints.auth.logout import logout as _logout
from web.blueprints.auth.register import register as _register
from web.decorators import require_auth, reject_auth


class AuthBlueprint:
    def __init__(self) -> None:
        self.blueprint: Blueprint = Blueprint("auth", __name__)

        self._setup()

    def _setup(self) -> None:
        @self.blueprint.route("/login", methods=["GET", "POST"])
        @reject_auth
        def login() -> Response | str:
            return _login()

        @self.blueprint.route("/logout")
        @require_auth
        def logout() -> Response:
            return _logout()

        @self.blueprint.route("/register", methods=["GET", "POST"])
        @reject_auth
        def register() -> Response | str:
            return _register()

    def get_blueprint(self) -> Blueprint:
        return self.blueprint
