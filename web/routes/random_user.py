from flask import redirect, url_for
from werkzeug import Response
from profile import random


def random_user() -> Response:
    return redirect(url_for(
        "user_profile",
        user_id=random()["user_id"]
    ))
