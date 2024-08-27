from flask import redirect, session, url_for
from werkzeug import Response
from messaging import Messages
import json

def conversation(recipient_id: int, ws) -> Response | None:
    if ("user_id") not in session:
        return redirect(url_for("auth.login"))

    messages = Messages(int(session["user_id"]), recipient_id)
    while True:
        check_sock(ws, messages)


def check_sock(ws, messages) -> None:
    received: str | None = ws.receive()
    if received: # if a request is received from the client
        res_json: dict = json.loads(received)

        if res_json["type"] == "get": # if the request is a 'get' request
            if res_json["resource"] == "messages": # if the client is requesting all messages
                ws.send(json.dumps({
                    "type": "post",
                    "resource": "messages",
                    "data": messages.get_messages()
                }))
        elif res_json["type"] == "post": # if the request is a 'post' request
            if res_json["resource"] == "messages": # if the user sent a new message
                messages.add_message(res_json["data"])

                ws.send(json.dumps({
                    "type": "post",
                    "resource": "messages",
                    "data": messages.get_messages()[-1]
                }))

