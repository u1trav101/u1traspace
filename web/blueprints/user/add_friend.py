from werkzeug import Response
from flask import redirect, url_for, session
from flask_wtf import FlaskForm
from web.forms import friend_form
from profile import send_friend_request


def _add_friend(recipient_id: int) -> Response:
    form: FlaskForm = friend_form()
    sender_id: int = int(session["user_id"])

    if form.validate_on_submit():
        if sender_id != recipient_id:
            approved: bool = send_friend_request(sender_id, recipient_id)

            if approved:
                return redirect(url_for("user.friends", user_id=session["user_id"]))
    
    return redirect(url_for("user.page", user_id=recipient_id))
