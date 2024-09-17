from flask import Blueprint
from werkzeug import Response
from web.decorators import require_auth
from web.blueprints.message.browse import _browse


message_blueprint = Blueprint("message", __name__)


@message_blueprint.route("/")
@require_auth
def browse() -> Response | str:
    return _browse()
