from flask import redirect, session, request, url_for
from werkzeug import Response


def _logout() -> Response:
    session.pop("user_id")

    if request.referrer is None or url_for("auth.logout") in request.referrer:
        return redirect(url_for("index"))

    return redirect(request.referrer)
