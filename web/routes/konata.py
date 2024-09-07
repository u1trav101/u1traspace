from flask import session, redirect, url_for
from werkzeug import Response


def konata() -> Response:
    if ("konata") in session:
        session.pop("konata")
    else:
        session["konata"] = True

    return redirect(url_for("user-list"))
