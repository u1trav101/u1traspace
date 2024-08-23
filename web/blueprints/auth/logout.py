from flask import redirect, session, request, url_for
from werkzeug import Response


def _logout() -> Response:
    if ("user_id") in session:
        session.pop("user_id")

    if request.referrer is None or url_for("auth.logout") in request.referrer:
        return redirect(url_for("auth.login"))

    return redirect(request.referrer)
