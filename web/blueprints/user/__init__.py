from flask import Blueprint
from werkzeug import Response
from web.decorators import validate_url_vars
from web.blueprints.user.browse import _browse
from web.blueprints.user.random import _random
from web.blueprints.user.page import _page


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/")
def browse() -> str:
    return _browse()


@user_blueprint.route("/random")
def random() -> Response:
    return _random()


@user_blueprint.route("/<user_id>/", methods=["GET", "POST"])
@validate_url_vars
def page(user_id: int) -> Response | str | tuple:
    return _page(user_id)
