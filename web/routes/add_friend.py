from flask import redirect, url_for, session
from web.forms import friend_form
from profile import send_friend_request


def add_friend(user_id):
    if ("user_id") not in session:
        return redirect(url_for("login"))

    try:
        int(user_id)
    except ValueError:
        return redirect(url_for("user_profile", user_id=user_id))

    form = friend_form()

    if form.validate_on_submit():
        if session["user_id"] != user_id:
            send_friend_request(session["user_id"], user_id)

            return redirect(url_for("user_profile", user_id=user_id))
