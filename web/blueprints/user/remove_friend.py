from flask import session, redirect, url_for, request
from flask_wtf import FlaskForm
from werkzeug import Response
from web.forms import friend_form
from db import Query


def _remove_friend(user_id: int) -> Response:
    if ("user_id") not in session:
        return redirect(url_for("auth.login"))

    form: FlaskForm = friend_form()

    if form.validate_on_submit():
        query = Query()
        query.friend_reject_action(session["user_id"], user_id)
        query.friend_reject_action(user_id, session["user_id"])
    
    if request.referrer is None or url_for("user.remove_friend", user_id=user_id) in request.referrer:
        return redirect(url_for("user.friend_list", user_id=session["user_id"]))
    
    return redirect(request.referrer)
