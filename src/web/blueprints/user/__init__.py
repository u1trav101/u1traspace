from flask import Blueprint
from werkzeug import Response
from web.decorators import validate_url_vars
from web.blueprints.user.browse import browse as _browse
from web.blueprints.user.random import random as _random
from web.blueprints.user.page import page as _page


class UserBlueprint:
    def __init__(self) -> None:
        self.blueprint = Blueprint("user", __name__)

        self._setup()

    def _setup(self) -> None:
        @self.blueprint.route("/")
        def browse() -> str:
            return _browse()

        @self.blueprint.route("/random")
        def random() -> Response:
            return _random()

        @self.blueprint.route("/<user_id>/", methods=["GET", "POST"])
        @validate_url_vars
        def page(user_id: int) -> Response | str | tuple:
            return _page(user_id)

    def get_blueprint(self) -> Blueprint:
        return self.blueprint
