from flask import Blueprint
from werkzeug import Response
from web.decorators import validate_url_vars
from web.blueprints.blog.browse import _browse
from web.blueprints.blog.post import _post
from web.blueprints.blog.new import _new


blog_blueprint = Blueprint("blog", __name__)

@blog_blueprint.route("/")
@validate_url_vars
def browse(user_id: int) -> Response | str:
    return _browse(user_id)

@blog_blueprint.route("/<post_id>/", methods=["GET", "POST"])
@validate_url_vars
def post(user_id: int, post_id: int) -> Response | str | tuple:
    return _post(user_id, post_id)

@blog_blueprint.route("/new/", methods=["GET", "POST"])
@validate_url_vars
def new(user_id: int) -> Response | str | tuple:
    return _new(user_id)