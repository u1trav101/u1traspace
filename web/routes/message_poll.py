from flask import redirect, request, session
from werkzeug import Response
import messaging


def message_poll(recipient_id: int) -> Response | list:
    if ("user_id") not in session:
        return redirect("login")

    time = request.args.get("t")
    if not time:
        return [False, 400, "Missing URL parameter 't'"]
    try:
        int(time)
    except ValueError:
        return [False, 400, "Invalid value for URL parameter 't'"]
    
    return messaging.poll_incoming_messages(session["user_id"], recipient_id, int(time))
