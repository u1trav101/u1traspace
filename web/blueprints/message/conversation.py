from flask import session
from werkzeug import Response
from messaging import Messages
import json

def conversation(recipient_id: int, ws) -> Response | None:
    messages = Messages(int(session["user_id"]), recipient_id)
    while True:
        check_sock(ws, messages)


def check_sock(ws, messages) -> None:
    received: str | None = ws.receive()
    if received: # if a request is received from the client
        res_json: dict = json.loads(received)

        match res_json["type"]:
            case "get": # if the client has sent data
                if res_json["resource"] == "messages": # if the client is requesting all messages
                    ws.send(json.dumps({
                        "type": "post",
                        "resource": "messages",
                        "data": messages.get_messages()
                    }))

            case "post": # if the client sent a request for all data
                if res_json["resource"] == "messages": # if the user sent a new message
                    messages.add_message(res_json["data"])
                    messages.refresh()

                    ws.send(json.dumps({
                        "type": "post",
                        "resource": "messages",
                        "data": messages.get_messages()[-1]
                    }))

            case "poll": # if the client is polling new messages
                if res_json["resource"] == "messages":
                    last_index = messages.get_last_index()
                    messages.refresh()

                    if messages.get_is_new_messages():
                        messages.set_is_new_messages(False)
                        
                        ws.send(json.dumps({
                            "type": "post",
                            "resource": "messages",
                            "data": messages.get_messages()[last_index + 1:]
                        }))

