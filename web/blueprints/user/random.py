from flask import redirect, url_for
from werkzeug import Response
import profile


def random() -> Response:
    return redirect(url_for("user.page", user_id=profile.random()["user_id"]))
