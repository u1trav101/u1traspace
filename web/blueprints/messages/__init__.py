from flask import Blueprint
from flask_sock import Sock
from werkzeug import Response
from web.decorators import require_auth, validate_url_vars
from web.blueprints.messages.browse import browse as _browse
from web.blueprints.messages.conversation import conversation as _conversation


class MessagesBlueprint:
    def __init__(self, sock: Sock) -> None:
        self.blueprint: Blueprint = Blueprint("messages", __name__)
        self.sock: Sock = sock

        self._setup()

    def _setup(self) -> None:
        @self.blueprint.route("/")
        @require_auth
        def browse() -> Response | str:
            return _browse()

        @self.sock.route("/<user_id>", self.blueprint)
        @validate_url_vars
        @require_auth
        def conversation(ws, user_id) -> Response | None:
            return _conversation(user_id, ws)

    def get_blueprint(self) -> Blueprint:
        return self.blueprint
