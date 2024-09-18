from flask import Blueprint
from werkzeug import Response
from web.decorators import require_auth
from web.blueprints.messages.browse import _browse


message_blueprint = Blueprint("messages", __name__)


@message_blueprint.route("/")
@require_auth
def browse() -> Response | str:
    return _browse()
