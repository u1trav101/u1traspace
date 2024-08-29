from flask_wtf import FlaskForm
from werkzeug import Response
from cdn import copy_default_avatar
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

        copy_default_avatar.delay(user_id)

        return forms.register_commit(user_id)

    return render_template(
        "auth/register.html",
        form=register_form,
    )