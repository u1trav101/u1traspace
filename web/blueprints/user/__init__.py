from flask import Blueprint, redirect, url_for
from werkzeug import Response
from web.misc import validate_url_vars
from web.blueprints.user.random import _random
from web.blueprints.user.page import _page
from web.blueprints.user.friends import _friends
from web.blueprints.user.add_friend import _add_friend
from web.blueprints.user.remove_friend import _remove_friend


user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/")
def redirect_to_user_list() -> Response:
    return redirect(url_for("user_list"))

@user_blueprint.route("/random/")
def random() -> Response:
    return _random()

@user_blueprint.route("/<user_id>/", methods=["GET", "POST"])
@validate_url_vars
def page(user_id: int) -> Response | str | tuple:
    return _page(user_id)

@user_blueprint.route("/<user_id>/friends/")
@validate_url_vars
def friends(user_id: int) -> Response | str:
    return _friends(user_id)

@user_blueprint.route("/<user_id>/add-friend/", methods=["POST"])
@validate_url_vars
def add_friend(user_id: int) -> Response:
    return _add_friend(user_id)

@user_blueprint.route("/<user_id>/remove-friend/", methods=["POST"])
@validate_url_vars
def remove_friend(user_id: int) -> Response:
    return _remove_friend(user_id)