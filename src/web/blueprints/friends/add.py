from werkzeug import Response
from flask import redirect, url_for, session
from flask_wtf import FlaskForm
from web.forms import blank_form
from profile import send_friend_request


def add(recipient_id: int) -> Response:
    friend_form: FlaskForm = blank_form()
    sender_id: int = int(session["user_id"])

    if friend_form.validate_on_submit():
        if sender_id != recipient_id:
            approved: bool = send_friend_request(sender_id, recipient_id)

            if approved:
                return redirect(
                    url_for("user.friends.browse", user_id=session["user_id"])
                )

    return redirect(url_for("user.page", user_id=recipient_id))
