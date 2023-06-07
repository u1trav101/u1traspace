from flask import session, redirect, url_for, request
from web.misc import render_template
from profile import get_all_notifications, get_profile_properties
from web.forms import notification_action_form
from tasks import handle_notification


def notifications():
    if ("user_id") not in session:
        return redirect(url_for("login"))

    action_form = notification_action_form()
    if action_form.validate_on_submit():
        res = request.form.get("action")

        handle_notification.delay(res)

        return redirect(url_for("notifications"))

    return render_template(
        "notifications.html",
        notifications=get_all_notifications(session["user_id"]),
        properties=get_profile_properties(session["user_id"]),
        form=action_form
    )
