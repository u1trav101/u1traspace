from flask import session, redirect, url_for, request
from flask_wtf import FlaskForm
from werkzeug import Response
from web.forms import blank_form
from db import Query


def remove(user_id: int) -> Response:
    friend_form: FlaskForm = blank_form()
    if friend_form.validate_on_submit():
        res: str | None = request.form.get("friend")
        if res:
            try:
                friend_id = int(res)

                query = Query()
                friends = query.select_friends(friend_id=friend_id)

                if friends:
                    friend = friends[0]
                    if friend["sender_id"] == int(session["user_id"]) or friend[
                        "recipient_id"
                    ] == int(session["user_id"]):
                        query.delete_friend(friend_id)
            except ValueError:
                pass

    if (
        request.referrer is None
        or url_for("user.friends.remove", user_id=user_id) in request.referrer
    ):
        return redirect(url_for("user.friends.browse", user_id=session["user_id"]))

    return redirect(request.referrer)
