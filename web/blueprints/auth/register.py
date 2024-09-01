from flask import session, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from web.overloads import render_template
import web.forms as forms
import auth


def _register() -> Response | str:
    register_form: FlaskForm = forms.register_form()

    if register_form.validate_on_submit():
        # registration successful
        user_id: int = auth.register_user(
            register_form.email.data,
            register_form.username.data,
            register_form.password.data
        )

        session["user_id"] = int(user_id)

        return redirect(url_for("user.page", user_id=user_id))

    return render_template(
        "auth/register.html",
        forms = {
            "register": register_form
        }
    )
