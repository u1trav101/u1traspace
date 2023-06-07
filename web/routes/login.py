from flask import session, redirect, url_for
import web.forms as forms
import auth
from web.misc import render_template


def login():
    if ("user_id") in session:
        return redirect(url_for("user_profile", user_id=session["user_id"]))

    login_form = forms.login_form()

    if login_form.validate_on_submit():
        if auth.login_correct(login_form.id.data, login_form.password.data):
            # login successful
            return forms.login_commit(login_form.id.data)

        # login unsuccessful
        print(f"CHIYO: Unsuccessful login attempt from User ID: {login_form.id.data}")

    return render_template(
        "login.html",
        form=login_form
    )
