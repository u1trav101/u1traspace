import typing
from flask import Blueprint
from werkzeug import Response
from web.misc import validate_url_vars
from web.blueprints.message.conversation import _conversation
from web.blueprints.message.browse import _browse
from web.blueprints.message.poll import _poll


message_blueprint = Blueprint("message", __name__)

@message_blueprint.route("/")
def browse() -> Response | str:
    return _browse()

@message_blueprint.route("/<user_id>/", methods=["GET", "POST"])
@validate_url_vars
def conversation(user_id: int) -> Response | str:
    return _conversation(user_id)

@message_blueprint.route("/msg/<user_id>/poll")
@validate_url_vars
def poll(user_id: int) -> Response | typing.List:
    return _poll(user_id)