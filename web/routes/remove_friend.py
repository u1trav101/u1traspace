from flask import session, redirect, url_for, request
from flask_wtf import FlaskForm
from werkzeug import Response
from web.forms import blank_form
from db import Query


def remove_friend(friend_id: int) -> Response:
    friend_form: FlaskForm = blank_form()
    if friend_form.validate_on_submit():
        query = Query()
        query.remove_friend(friend_id)
    
    if request.referrer is None or url_for("remove_friend", friend_id=friend_id) in request.referrer:
        return redirect(url_for("user.friends", user_id=session["user_id"]))
    
    return redirect(request.referrer)
