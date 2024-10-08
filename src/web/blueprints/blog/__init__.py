from flask import Blueprint
from werkzeug import Response
from web.decorators import require_auth, require_ownership, validate_url_vars
from web.blueprints.blog.browse import browse as _browse
from web.blueprints.blog.post import post as _post
from web.blueprints.blog.new import new as _new


class BlogBlueprint:
    def __init__(self) -> None:
        self.blueprint: Blueprint = Blueprint("blog", __name__)

        self._setup()

    def _setup(self) -> None:
        @self.blueprint.route("/", methods=["GET", "POST"])
        @validate_url_vars
        def browse(user_id: int) -> Response | str:
            return _browse(user_id)

        @self.blueprint.route("/<post_id>", methods=["GET", "POST"])
        @validate_url_vars
        def post(user_id: int, post_id: int) -> Response | str | tuple:
            return _post(user_id, post_id)

        @self.blueprint.route("/new", methods=["GET", "POST"])
        @validate_url_vars
        @require_auth
        @require_ownership
        def new(user_id: int) -> Response | str | tuple:
            return _new(user_id)

    def get_blueprint(self) -> Blueprint:
        return self.blueprint
