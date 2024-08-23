from flask import redirect, url_for
from werkzeug import Response
from profile import random


def _random() -> Response:
    return redirect(url_for(
        "user.page",
        user_id=random()["user_id"]
    ))
