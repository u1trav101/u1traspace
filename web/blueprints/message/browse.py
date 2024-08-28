from flask import session, redirect, url_for
from werkzeug import Response
from web.overloads import render_template
import profile
import messaging

def _browse() -> Response | str:
    if ("user_id") not in session:
        return redirect(url_for("auth.login"))

    return render_template(
        "messagelist.html",
        conversations=messaging.get_user_conversations(int(session["user_id"])),
        friends=profile.get_user_friends(int(session["user_id"]))
    )