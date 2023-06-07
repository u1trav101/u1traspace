from flask import redirect, request, session
from tasks import clear_message_notifications
import messaging


def message_poll(recipient_id):
    if ("user_id") not in session:
        return redirect("login")

    try:
        int(recipient_id)
    except ValueError:
        return [False, 404, "404 - User does not exist"]

    clear_message_notifications.delay(session["user_id"], recipient_id)

    return messaging.poll_incoming_messages(session["user_id"], recipient_id, request.args.get("t"))
