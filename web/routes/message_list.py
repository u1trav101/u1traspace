from flask import session, redirect, url_for
from werkzeug import Response
from web.misc import render_template
import profile
import messaging

def message_list() -> Response | str:
    if ("user_id") not in session:
        return redirect(url_for("login"))

    return render_template(
        "messagelist.html",
        conversations=messaging.get_user_conversations(session["user_id"]),
        friends=profile.get_user_friends(session["user_id"])
    )