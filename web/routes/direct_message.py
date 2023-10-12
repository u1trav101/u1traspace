from flask import redirect, session, url_for
from db import Query
from web.misc import render_template
from tasks import clear_message_notifications
import web.forms as forms
import profile
import messaging


def direct_message(recipient_id):
    if ("user_id") not in session:
        return redirect(url_for("login"))

    try:
        int(recipient_id)
    except ValueError:
        return redirect(url_for("friend_list", user_id=session["user_id"]))

    clear_message_notifications.delay(session["user_id"], recipient_id)

    query = Query()
    friends = query.get_user_friends(recipient_id)

    are_friends = False
    for friend in friends:
        if int(session["user_id"]) == friend["friend"]:
            are_friends = True

    if not are_friends:
        return redirect(url_for("friend_list", user_id=session["user_id"]))

    message_form = forms.message_form()

    if message_form.validate_on_submit():
        messaging.send_message(
            session["user_id"],
            recipient_id,
            message_form.corpus.data
        )

        return redirect(url_for("direct_message", recipient_id=recipient_id))

    return render_template(
        "directmsg.html",
        properties=profile.get_profile_properties(recipient_id),
        messages=messaging.get_direct_messages(recipient_id, session["user_id"]),
        conversations=messaging.get_user_conversations(session["user_id"]),
        friends=profile.get_user_friends(session["user_id"]),
        form=message_form
    )
