from flask import session, redirect, url_for
from web.misc import render_template
from db import Query
import web.forms as forms
import auth


def login():
    if ("user_id") in session:
        return redirect(url_for("user_profile", user_id=session["user_id"]))

    login_form = forms.login_form()

    if login_form.validate_on_submit():
        if auth.login_correct(login_form.email.data, login_form.password.data):
            # login successful
            query = Query()
            user_id = query.select_users(email=login_form.email.data, limit=1)[0]["user_id"]
            session["user_id"] = str(user_id)
            
            return redirect(url_for("user_profile", user_id=user_id))

    return render_template(
        "login.html",
        form=login_form
    )
