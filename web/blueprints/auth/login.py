from flask import session, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from web.overloads import render_template
from db import Query
import web.forms as forms
import auth


def _login() -> Response | str:
    login_form: FlaskForm = forms.login_form()

    if login_form.validate_on_submit():
        if auth.login_correct(login_form.email.data, login_form.password.data):
            # login successful
            query = Query()
            user_id: int = query.select_users(email=login_form.email.data, limit=1)[0]["user_id"]
            session["user_id"] = str(user_id)
            
            return redirect(url_for("user.page", user_id=user_id))

    return render_template(
        "login.html",
        form=login_form
    )
