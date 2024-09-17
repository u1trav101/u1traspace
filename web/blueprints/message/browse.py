from flask import session
from werkzeug import Response
from web.overloads import render_template
from profile import get_user_friends
from messaging import get_user_conversations


def _browse() -> Response | str:
    return render_template(
        "message/browse.html",
        conversations=get_user_conversations(int(session["user_id"])),
        friends=get_user_friends(int(session["user_id"])),
    )
