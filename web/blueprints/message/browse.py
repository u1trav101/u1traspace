from flask import session
from werkzeug import Response
from web.overloads import render_template
import profile
import messaging

def _browse() -> Response | str:
    return render_template(
        "message/browse.html",
        conversations=messaging.get_user_conversations(int(session["user_id"])),
        friends=profile.get_user_friends(int(session["user_id"]))
    )