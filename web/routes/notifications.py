from flask import session, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from web.misc import render_template
from profile import get_profile_properties
from web.forms import notification_action_form


def notifications() -> Response | str:
    if ("user_id") not in session:
        return redirect(url_for("login"))

    action_form: FlaskForm = notification_action_form()

    return render_template(
        "notifications.html",
        properties=get_profile_properties(session["user_id"]),
        form=action_form
    )
