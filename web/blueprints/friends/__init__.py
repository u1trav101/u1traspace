from flask import Blueprint
from werkzeug import Response
from web.decorators import validate_url_vars, require_auth
from web.blueprints.friends.browse import browse as _browse
from web.blueprints.friends.add import add as _add
from web.blueprints.friends.remove import remove as _remove

friend_blueprint = Blueprint("friends", __name__)


@friend_blueprint.route("/")
@validate_url_vars
def browse(user_id: int) -> Response | str:
    return _browse(user_id)


@friend_blueprint.route("/add", methods=["POST"])
@validate_url_vars
@require_auth
def add(user_id: int) -> Response:
    return _add(user_id)


@friend_blueprint.route("/remove", methods=["POST"])
@require_auth
@validate_url_vars
def remove(user_id: int) -> Response:
    return _remove(user_id)
