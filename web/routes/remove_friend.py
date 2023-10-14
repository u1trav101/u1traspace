from flask import session, redirect, url_for, request
from web.forms import friend_form
from db import Query


def remove_friend(user_id):
    if ("user_id") not in session:
        return redirect(url_for("login"))

    try:
        int(user_id)
    except ValueError:
        return redirect(url_for("friend_list", user_id=session["user_id"]))

    form = friend_form()

    if form.validate_on_submit():
        query = Query()
        query.friend_reject_action(session["user_id"], user_id)
        query.friend_reject_action(user_id, session["user_id"])
    
    print(request.referrer)
    if request.referrer is None or url_for("remove_friend", user_id=user_id) in request.referrer:
        return redirect(url_for("friend_list", user_id=session["user_id"]))
    
    return redirect(request.referrer)
