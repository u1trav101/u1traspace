from flask import redirect, url_for, session
from web.forms import friend_form
from profile import send_friend_request


def add_friend(recipient_id):
    if ("user_id") not in session:
        return redirect(url_for("login"))

    try:
        int(recipient_id)
    except ValueError:
        return redirect(url_for("user_profile", user_id=recipient_id))

    form = friend_form()
    sender_id = session["user_id"]

    if form.validate_on_submit():
        if sender_id != recipient_id:
            approved = send_friend_request(sender_id, recipient_id)

            return redirect(url_for("friend_list", user_id=session["user_id"])) if approved \
                else redirect(url_for("user_profile", user_id=recipient_id))
