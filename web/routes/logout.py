from flask import redirect, session, request, url_for
from werkzeug import Response


def logout() -> Response:
    if ("user_id") in session:
        session.pop("user_id")

    if request.referrer is None or url_for("logout") in request.referrer:
        return redirect(url_for("login"))

    return redirect(request.referrer)
